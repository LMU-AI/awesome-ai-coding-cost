#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 README 里收录的仓库是否过期。

用法:
    python3 scripts/check_entries.py              # 检查并打印报告
    python3 scripts/check_entries.py --fix        # 同时把 star/更新日期写回 README

判定规则（与 README 的收录标准一致）:
    - 最后更新超过 90 天  -> STALE，README 里必须标注「已停更」
    - star 数与 README 记录相差超过 20%  -> 数字过期，建议更新
    - 仓库 404 / 改名      -> DEAD，应移除或更正链接

不需要 token 也能跑，但匿名调用 GitHub API 限速 60 次/小时。
设置 GITHUB_TOKEN 环境变量可提到 5000 次/小时：
    GITHUB_TOKEN=ghp_xxx python3 scripts/check_entries.py
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

README = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
STALE_DAYS = 90
STAR_DRIFT = 0.20

# 维护方自己的仓库：不参与 star 校验（README 里用 — 占位）
OWN_PREFIX = "LMU-AI/"


def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-ai-coding-cost-checker",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"__error__": e.code}
    except Exception as e:  # 网络问题等
        return {"__error__": str(e)}


def parse_rows(text):
    """抓表格行：| [owner/repo](url) | star | license | date | desc |"""
    rows = []
    pattern = re.compile(
        r"^\|\s*\[([^\]]+)\]\(https://github\.com/([\w.\-]+/[\w.\-]+)\)\s*\|"
        r"\s*([\d,]+|—|-)\s*\|\s*([^|]+?)\s*\|\s*([\d]{4}-[\d]{2}-[\d]{2}|—|-)\s*\|",
        re.M,
    )
    for m in pattern.finditer(text):
        stars = m.group(3).replace(",", "")
        rows.append(
            {
                "label": m.group(1),
                "repo": m.group(2),
                "stars": int(stars) if stars.isdigit() else None,
                "license": m.group(4).strip(),
                "updated": m.group(5) if m.group(5) not in ("—", "-") else None,
                "raw": m.group(0),
            }
        )
    return rows


def main():
    fix = "--fix" in sys.argv
    text = open(README, encoding="utf-8").read()
    rows = parse_rows(text)
    if not rows:
        print("⚠️  没有从 README 解析到任何条目，检查表格格式是否改动过")
        return 1

    print("解析到 %d 个条目\n" % len(rows))
    now = datetime.now(timezone.utc)
    problems = []
    new_text = text

    for r in rows:
        repo = r["repo"]
        if repo.startswith(OWN_PREFIX):
            print("  ⏭  %-46s 自有仓库，跳过 star 校验" % repo)
            continue

        d = api("/repos/" + repo)
        if "__error__" in d:
            code = d["__error__"]
            if code == 404:
                problems.append((repo, "DEAD", "仓库 404，可能已删除或改名"))
                print("  ❌ %-46s 404" % repo)
            elif code == 403:
                print("  ⚠️  %-46s API 限速，设置 GITHUB_TOKEN 后重试" % repo)
            else:
                print("  ⚠️  %-46s 请求失败: %s" % (repo, code))
            continue

        live_stars = d["stargazers_count"]
        pushed = d["pushed_at"][:10]
        age = (now - datetime.strptime(d["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)).days
        flags = []

        if age > STALE_DAYS:
            flags.append("STALE(%d天未更新)" % age)
            problems.append((repo, "STALE", "%d 天未更新，README 需标注已停更" % age))

        if r["stars"] and live_stars:
            drift = abs(live_stars - r["stars"]) / float(r["stars"])
            if drift > STAR_DRIFT:
                flags.append("star %d→%d (%+.0f%%)" % (r["stars"], live_stars, drift * 100))
                problems.append((repo, "STARS", "README 记 %d，实际 %d" % (r["stars"], live_stars)))

        if r["updated"] and r["updated"] != pushed:
            flags.append("日期 %s→%s" % (r["updated"], pushed))

        if fix:
            fixed = r["raw"]
            if r["stars"] and live_stars != r["stars"]:
                fixed = fixed.replace("| %d |" % r["stars"], "| %d |" % live_stars, 1)
            if r["updated"] and r["updated"] != pushed:
                fixed = fixed.replace(r["updated"], pushed, 1)
            if fixed != r["raw"]:
                new_text = new_text.replace(r["raw"], fixed, 1)

        status = "⚠️ " if flags else "✅"
        print("  %s %-46s %6d★  upd=%s  %s" % (status, repo, live_stars, pushed, " | ".join(flags)))

    if fix and new_text != text:
        open(README, "w", encoding="utf-8").write(new_text)
        print("\n✍️  已把 star 与更新日期写回 README")

    print("\n" + "=" * 64)
    if problems:
        print("需要处理 %d 项：\n" % len(problems))
        for repo, kind, msg in problems:
            print("  [%s] %-44s %s" % (kind, repo, msg))
        print("\n⚠️  别忘了同步改 README 顶部的「数据核实时间」")
        return 1
    print("✅ 全部条目有效，无需处理")
    print("⚠️  仍需手动确认：README 顶部的「数据核实时间」是否为今天")
    return 0


if __name__ == "__main__":
    sys.exit(main())
