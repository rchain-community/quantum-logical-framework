#!/usr/bin/env python3
"""Document-network check (issue #149).

QLF is 180 root Markdown files plus lean/README.md, and readability means a reader following
a claim always lands on its proof or its parent doc. Three things are checked, all cheap:

  1. Orphans   -- every root .md except README.md must be named by at least one OTHER .md.
  2. Dead links -- every relative Markdown link, in every .md file, must resolve on disk.
                   (tools/flowchart_source.md is resolved from the repo root, because the
                   builder emits it as FlowChart.md there.)
  3. Back-links -- warning only: an X.md with an X.py or lean/QLF_X.lean of the same name
                   should mention it, and vice versa. Reported, not fatal, because the pairing
                   is by name alone and a few legitimate pairs are documented elsewhere.

Exit status is non-zero on any orphan or dead link, so this can gate CI.

    python3 scripts/doc_network_check.py            # report
    python3 scripts/doc_network_check.py --quiet    # only failures
"""
import glob
import os
import re
import sys
import urllib.parse

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

QUIET = "--quiet" in sys.argv

LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
SKIP_PREFIX = ("http://", "https://", "mailto:", "#")


def all_markdown():
    return sorted(p for p in glob.glob("**/*.md", recursive=True)
                  if not p.startswith((".lake", ".git")) and "/.lake/" not in p)


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def check_orphans(texts):
    roots = [p for p in texts if "/" not in p and p != "README.md"]
    return [m for m in roots if not any(m in t for p, t in texts.items() if p != m)]


def check_links(texts):
    dead = {}
    n = 0
    for p, t in texts.items():
        base = "." if p == "tools/flowchart_source.md" else os.path.dirname(p)
        for m in LINK.finditer(t):
            target = m.group(1)
            if target.startswith(SKIP_PREFIX):
                continue
            n += 1
            path = urllib.parse.unquote(target.split("#")[0])
            if not path or ('.' not in path and '/' not in path):
                continue  # not a path: e.g. TeX `\mathcal{M}[f](s)` matching the link syntax
            if not os.path.exists(os.path.normpath(os.path.join(base, path))):
                dead.setdefault(p, []).append(target)
    return n, dead


def check_backlinks(texts):
    def norm(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())
    roots = {os.path.splitext(p)[0]: p for p in texts if "/" not in p}
    pys = {os.path.splitext(p)[0]: p for p in glob.glob("*.py")}
    leans = {p[len("lean/QLF_"):-len(".lean")]: p for p in glob.glob("lean/QLF_*.lean")}
    out = []
    for b, md in sorted(roots.items()):
        if b in pys:
            py = pys[b]
            if py not in texts[md]:
                out.append(f"{md} does not mention {py}")
            if md not in read(py):
                out.append(f"{py} does not mention {md}")
    byn = {norm(b): (b, p) for b, p in roots.items()}
    for lb, lp in sorted(leans.items()):
        if norm(lb) in byn:
            b, md = byn[norm(lb)]
            if os.path.basename(lp) not in texts[md] and lb not in texts[md]:
                out.append(f"{md} does not mention {lp}")
            if md not in read(lp):
                out.append(f"{lp} does not mention {md}")
    return out


def main():
    texts = {p: read(p) for p in all_markdown()}
    orphans = check_orphans(texts)
    n_links, dead = check_links(texts)
    backlinks = check_backlinks(texts)

    if not QUIET:
        print(f"markdown files: {len(texts)}   relative links: {n_links}")
    if orphans:
        print("ORPHANS (no incoming link from any other .md):")
        for m in orphans:
            print("   ", m)
    if dead:
        print("DEAD LINKS:")
        for p, ts in sorted(dead.items()):
            for t in sorted(set(ts)):
                print(f"    {p}: {t}")
    if backlinks and not QUIET:
        print("back-link gaps (warning only):")
        for b in backlinks:
            print("   ", b)
    ok = not orphans and not dead
    if not QUIET:
        print("OK" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
