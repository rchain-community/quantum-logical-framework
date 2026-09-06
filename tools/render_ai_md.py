#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a Markdown doc (default: AI.md) to a standalone styled HTML page,
tuned for copy/paste into Google Docs.

    python3 tools/render_ai_md.py                  # AI.md  -> AI.html
    python3 tools/render_ai_md.py Millennium.md    # -> Millennium.html
    python3 tools/render_ai_md.py AI.md -o /tmp/ai.html

The output opens in a browser with a "Copy for Google Docs" button that selects
the rendered article and copies it as rich text — paste straight into a Doc.

Why a bespoke converter rather than pandoc: the text is dense with the twist
alphabet (^ v < > / \\ + -), so < > & escaping has to be exact, and Google Docs'
paste-table importer ignores CSS width but respects an explicit <col> width
attribute — so every table gets a <colgroup> with per-column percentages
auto-sized from its content. Chips/badges are avoided (Docs mangles per-run
background/border); status text is plain bold. Reads the source file verbatim,
so it never drifts from the doc.
"""
import argparse
import html
import os
import re
import sys

PIPE = "\x00PIPE\x00"  # placeholder for escaped \| inside table cells


# --- inline ---------------------------------------------------------------

def inline(md: str) -> str:
    s = html.escape(md, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*\s][^*]*?)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s.replace(PIPE, "|")


def esc(s: str) -> str:
    return html.escape(s, quote=False).replace(PIPE, "|")


# --- tables -------------------------------------------------------------

def split_row(row: str):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.strip() for c in row.split("|")]


def col_widths(headers, rows):
    n = len(headers)
    weights = []
    for i in range(n):
        samples = [headers[i]] + [r[i] if i < len(r) else "" for r in rows]
        lens = [len(re.sub(r'[`*\[\]]|\(https?://[^)]+\)', '', s)) for s in samples]
        weights.append(max(sum(lens) / len(lens), 4))
    total = sum(weights)
    pct = [max(9, round(w / total * 100)) for w in weights]
    pct[pct.index(max(pct))] += 100 - sum(pct)
    return pct


def render_table(block):
    lines = [l for l in block if l.strip()]
    headers = split_row(lines[0])
    rows = [split_row(l) for l in lines[2:]]
    widths = col_widths(headers, rows)
    # Presentational `width` attribute, not inline `style`: Google Docs' paste
    # importer only reads the attribute, and HTML sanitizers (e.g. the Claude
    # artifact renderer) strip inline `style` — which silently drops every column
    # width and collapses `table-layout:fixed` to first-row sizing.
    colgroup = "<colgroup>" + "".join(f'<col width="{w}%">' for w in widths) + "</colgroup>"
    th = "".join(f"<th>{inline(h)}</th>" for h in headers)
    trs = []
    for r in rows:
        cells = "".join(f"<td>{inline(r[i]) if i < len(r) else ''}</td>" for i in range(len(headers)))
        trs.append(f"<tr>{cells}</tr>")
    return (f'<div class="table-wrap"><table>{colgroup}<thead><tr>{th}</tr>'
            f'</thead><tbody>{"".join(trs)}</tbody></table></div>\n')


# --- lists -------------------------------------------------------------

LIST_RE = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.*)$')


def render_list(items, ordered):
    tag = "ol" if ordered else "ul"
    lis = "".join(f"<li>{inline(t)}</li>\n" for t in items)
    return f"<{tag}>\n{lis}</{tag}>\n"


# --- block loop ------------------------------------------------------

def convert(md: str) -> str:
    md = md.replace(r"\|", PIPE)
    lines = md.split("\n")
    out = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            j = i + 1
            body = []
            while j < n and not lines[j].strip().startswith("```"):
                body.append(lines[j])
                j += 1
            out.append('<pre class="plain"><code>'
                       + "\n".join(esc(b) for b in body) + "</code></pre>\n")
            i = j + 1
            continue

        # horizontal rule
        if re.fullmatch(r'(-{3,}|\*{3,}|_{3,})', stripped):
            out.append('<hr class="sep">\n')
            i += 1
            continue

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                out.append('<p class="eyebrow">Quantum Logical Framework</p>\n')
                out.append(f"<h1>{inline(text)}</h1>\n")
            elif level == 2:
                anchor = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:40]
                out.append(f'<h2 id="{anchor}">{inline(text)}</h2>\n')
            else:
                out.append(f"<h{level}>{inline(text)}</h{level}>\n")
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            paras, cur = [], []
            for b in buf:
                if b.strip():
                    cur.append(b.strip())
                elif cur:
                    paras.append(" ".join(cur)); cur = []
            if cur:
                paras.append(" ".join(cur))
            inner = "".join(f"<p>{inline(pp)}</p>\n" for pp in paras)
            out.append(f'<div class="callout">{inner}</div>\n')
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and re.match(r'^\s*\|[\s:|-]+\|?\s*$', lines[i + 1]):
            block = []
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(render_table(block))
            continue

        # list
        if LIST_RE.match(line):
            ordered = bool(re.match(r'\d+\.', LIST_RE.match(line).group(2)))
            items = []
            while i < n:
                lm = LIST_RE.match(lines[i])
                if lm:
                    items.append(lm.group(3).strip())
                    i += 1
                elif lines[i].strip() and lines[i].startswith((" ", "\t")) and items:
                    items[-1] += " " + lines[i].strip()
                    i += 1
                elif not lines[i].strip():
                    k = i + 1
                    while k < n and not lines[k].strip():
                        k += 1
                    if k < n and LIST_RE.match(lines[k]):
                        i = k
                    else:
                        break
                else:
                    break
            out.append(render_list(items, ordered))
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip():
            s = lines[i].strip()
            if (s.startswith(("#", ">", "|", "```")) or re.fullmatch(r'(-{3,}|\*{3,})', s)
                    or LIST_RE.match(lines[i])):
                break
            buf.append(s)
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>\n")

    return "".join(out)


# --- page shell -----------------------------------------------------

HEAD = r"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{
  --paper:#F6F5FB; --paper-raise:#EEEBF9; --ink:#1C1A2B; --ink-soft:#55506E;
  --accent:#4B3AA4; --accent-ink:#FFFFFF; --warm:#A6690F;
  --line:#DAD6EC; --line-soft:#E7E4F3; --console-bg:#1D1930; --console-ink:#E7E4F7; --console-dim:#B9B2DC;
  --shadow:0 1px 2px rgba(28,26,43,0.06), 0 8px 24px -12px rgba(28,26,43,0.18);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#131024; --paper-raise:#1B1730; --ink:#EDEAF7; --ink-soft:#B4ADD4;
  --accent:#A796FF; --accent-ink:#17132B; --warm:#E8B562;
  --line:#33305A; --line-soft:#26223F; --console-bg:#0E0C1C; --console-ink:#E7E4F7; --console-dim:#9089B8;
  --shadow:0 1px 2px rgba(0,0,0,0.3), 0 8px 24px -12px rgba(0,0,0,0.5);
}}
:root[data-theme="dark"]{
  --paper:#131024; --paper-raise:#1B1730; --ink:#EDEAF7; --ink-soft:#B4ADD4;
  --accent:#A796FF; --accent-ink:#17132B; --warm:#E8B562;
  --line:#33305A; --line-soft:#26223F; --console-bg:#0E0C1C; --console-ink:#E7E4F7; --console-dim:#9089B8;
  --shadow:0 1px 2px rgba(0,0,0,0.3), 0 8px 24px -12px rgba(0,0,0,0.5);
}
*{box-sizing:border-box;}
body{background:var(--paper); color:var(--ink); margin:0;
  font-family:'IBM Plex Sans',ui-sans-serif,system-ui,sans-serif; font-size:16.5px; line-height:1.65;
  -webkit-font-smoothing:antialiased;}
::selection{background:var(--paper-raise); color:var(--ink);}
.page{max-width:940px; margin:0 auto; padding:56px 24px 96px;}
h1,h2,h3,h4,h5,h6{font-family:'Fraunces',Georgia,serif; text-wrap:balance; color:var(--ink);}
h1{font-size:clamp(2.1rem,5vw,3rem); font-weight:600; line-height:1.08; margin:0 0 14px; letter-spacing:-0.01em;}
h2{font-size:1.55rem; font-weight:600; margin:56px 0 18px; padding-top:28px; border-top:1px solid var(--line);}
h2:first-of-type{margin-top:40px;}
h3{font-size:1.2rem; font-weight:600; margin:34px 0 12px;}
h4{font-size:1.03rem; font-weight:600; margin:26px 0 10px; font-style:italic; color:var(--ink-soft);}
p{margin:0 0 16px; max-width:74ch;}
strong{font-weight:600; color:var(--ink);}
em{font-style:italic;}
a{color:var(--accent); text-decoration-thickness:1px; text-underline-offset:2px;}
a code{color:var(--accent);}
code{font-family:'IBM Plex Mono',ui-monospace,monospace; font-size:0.87em; background:var(--paper-raise);
  border:1px solid var(--line-soft); border-radius:4px; padding:0.05em 0.38em;}
ul,ol{margin:0 0 18px; padding-left:1.4em; max-width:74ch;}
li{margin:0 0 9px;} li::marker{color:var(--accent);}
.eyebrow{font-family:'IBM Plex Mono',monospace; font-size:0.76rem; letter-spacing:0.14em; text-transform:uppercase;
  color:var(--accent); margin:0 0 14px;}
.callout{border:1px solid var(--line); border-left:3px solid var(--accent); background:var(--paper-raise);
  border-radius:6px; padding:14px 20px; margin:0 0 18px;}
.callout p{margin:0 0 10px; max-width:none;} .callout p:last-child{margin-bottom:0;}
pre.plain{background:var(--console-bg); color:var(--console-ink); border-radius:8px; padding:18px 20px;
  overflow-x:auto; font-family:'IBM Plex Mono',monospace; font-size:0.84rem; line-height:1.6;
  box-shadow:var(--shadow); margin:0 0 20px; white-space:pre;}
pre.plain code{background:none; border:0; padding:0; color:inherit; font-size:1em; white-space:pre;}
.table-wrap{overflow-x:auto; margin:0 0 20px; border:1px solid var(--line); border-radius:8px;}
table{border-collapse:collapse; width:100%; font-size:0.92rem; min-width:640px; table-layout:fixed;}
thead th{text-align:left; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; letter-spacing:.06em;
  text-transform:uppercase; color:var(--ink-soft); background:var(--paper-raise); padding:11px 14px;
  border-bottom:1px solid var(--line); word-wrap:break-word;}
tbody td{padding:13px 14px; border-bottom:1px solid var(--line-soft); vertical-align:top; word-wrap:break-word;}
tbody tr:last-child td{border-bottom:0;}
.table-wrap code{background:none; border:0; padding:0; border-radius:0;}
hr.sep{border:0; border-top:1px solid var(--line); margin:40px 0;}
footer.colophon{margin-top:64px; padding-top:22px; border-top:1px solid var(--line);
  font-family:'IBM Plex Mono',monospace; font-size:0.78rem; color:var(--ink-soft);
  display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px;}
.copybar{position:fixed; top:14px; right:14px; z-index:50; display:flex; gap:8px;}
.copybar button{font:600 0.8rem/1 'IBM Plex Mono',monospace; letter-spacing:.03em; cursor:pointer;
  color:var(--accent-ink); background:var(--accent); border:1px solid var(--accent);
  border-radius:6px; padding:9px 14px; box-shadow:var(--shadow);}
.copybar button:focus-visible{outline:2px solid var(--accent); outline-offset:2px;}
.copybar .done{background:transparent; color:var(--accent);}
@media print{.copybar{display:none;}}
</style>
"""

SCRIPT = r"""<script>
(function(){
  var btn = document.getElementById('copybtn');
  if(!btn) return;
  btn.addEventListener('click', function(){
    var art = document.getElementById('doc');
    var sel = window.getSelection();
    sel.removeAllRanges();
    var r = document.createRange();
    r.selectNodeContents(art);
    sel.addRange(r);
    var ok = false;
    try { ok = document.execCommand('copy'); } catch(e){ ok = false; }
    sel.removeAllRanges();
    btn.textContent = ok ? 'Copied ✓' : 'Press ⌘/Ctrl+C';
    btn.classList.toggle('done', ok);
    setTimeout(function(){ btn.textContent = 'Copy for Google Docs'; btn.classList.remove('done'); }, 2600);
  });
})();
</script>
"""


def build_page(md: str, title: str) -> str:
    body = convert(md)
    return (
        HEAD.replace("__TITLE__", html.escape(title, quote=True))
        + '<div class="copybar"><button id="copybtn">Copy for Google Docs</button></div>\n'
        + '<article id="doc" class="page">\n' + body
        + '<footer class="colophon"><span>Quantum Logical Framework</span>'
        + '<span>rchain-community/quantum-logical-framework</span></footer>\n</article>\n'
        + SCRIPT
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("source", nargs="?", default=os.path.join(repo, "AI.md"),
                    help="Markdown file to render (default: AI.md at repo root)")
    ap.add_argument("-o", "--out", help="output HTML path (default: <source>.html in cwd)")
    ap.add_argument("-t", "--title", help="page <title> (default: the doc's first H1)")
    args = ap.parse_args()

    with open(args.source, encoding="utf-8") as f:
        md = f.read()

    title = args.title
    if not title:
        m = re.search(r'^#\s+(.+)$', md, re.M)
        title = m.group(1).strip() if m else os.path.basename(args.source)

    out = args.out or (os.path.splitext(os.path.basename(args.source))[0] + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build_page(md, title))
    print(f"wrote {out}  ({os.path.getsize(out):,} bytes)  title: {title!r}")


if __name__ == "__main__":
    main()
