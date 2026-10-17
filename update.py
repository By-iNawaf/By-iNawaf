#!/usr/bin/env python3
"""Builds assets/stats.svg + assets/project-N.svg from the GitHub API.
Run by the daily GitHub Action. Offline test:  python scripts/update.py --offline"""
import json, os, sys, html, urllib.request

USER = "By-iNawaf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_PROJECTS = 6
LANG = {"JavaScript":"#f1e05a","Python":"#3572A5","TypeScript":"#3178c6","C#":"#178600",
        "C++":"#f34b7d","HTML":"#e34c26","CSS":"#563d7c","Java":"#b07219","Go":"#00ADD8","Shell":"#89e051"}

CSS = """:root{--g:#00ff88;--c:#00e5ff;--t:#e6edf3;--d:#8b949e}
@media (prefers-color-scheme:light){:root{--g:#00b868;--c:#0096b4;--t:#1f2328;--d:#57606a}}
text{font-family:"Segoe UI","SF Pro Arabic","Geeza Pro",Tahoma,Arial,sans-serif}
.mono{font-family:ui-monospace,"SF Mono",Consolas,monospace}
.t{fill:var(--t)}.d{fill:var(--d)}.g{fill:var(--g)}.gr{fill:url(#gr)}
.sp{stroke:var(--g);stroke-opacity:.25;stroke-width:1;stroke-dasharray:2 5}"""
DEFS = """<linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--g)"/><stop offset="1" style="stop-color:var(--c)"/></linearGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" style="stop-color:var(--g)" stop-opacity="0"/><stop offset=".5" style="stop-color:var(--g)"/><stop offset="1" style="stop-color:var(--c)" stop-opacity="0"/></linearGradient>
<filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>"""

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{DEFS}</defs><style>{CSS}</style>{body}</svg>')

def load():
    if "--offline" not in sys.argv:
        try:
            h = {"Accept": "application/vnd.github+json", "User-Agent": "profile-updater"}
            if os.environ.get("GITHUB_TOKEN"):
                h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
            get = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=20))
            user = get(f"https://api.github.com/users/{USER}")
            repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
            return {"public_repos": user["public_repos"], "repos": repos}
        except Exception as e:
            print("API failed, using data/repos.json:", e)
    return json.load(open(os.path.join(ROOT, "data", "repos.json"), encoding="utf-8"))

def counter(n, x, y, size=64):
    """number that counts up once on load (pure SVG, no JS)"""
    d = 1.3 / max(n, 1); out = ""
    for k in range(n + 1):
        last = k == n
        sets = f'<set attributeName="opacity" to="1" begin="{k*d:.3f}s" fill="freeze"/>'
        if not last:
            sets += f'<set attributeName="opacity" to="0" begin="{(k+1)*d:.3f}s" fill="freeze"/>'
        out += (f'<text class="cnt{" last" if last else ""} mono gr" opacity="0" x="{x}" y="{y}" text-anchor="middle" '
                f'font-size="{size}" font-weight="800" filter="url(#gl)">{k}{sets}</text>')
    return out

def stats(data, projects):
    stars = sum(r.get("stargazers_count") or 0 for r in data["repos"])
    langs = len({r["language"] for r in data["repos"] if r.get("language")})
    items = [(data["public_repos"], "REPOSITORIES"), (stars, "STARS"), (langs, "LANGUAGES")]
    b = ""
    for i, (n, label) in enumerate(items):
        cx = 133 + i * 267
        b += counter(n, cx, 92)
        b += f'<text x="{cx}" y="128" text-anchor="middle" class="d mono" font-size="14" letter-spacing="5">{label}</text>'
        b += (f'<rect x="{cx-45}" y="142" width="90" height="2" fill="url(#ln)"><animate attributeName="width" '
              f'values="0;90" dur="1.2s" fill="freeze"/><animate attributeName="x" values="{cx};{cx-45}" dur="1.2s" fill="freeze"/></rect>')
        if i < 2:
            b += f'<path d="M{cx+133} 44V132" class="sp" fill="none"/>'
    return svg(800, 170, b)

def project(i, r):
    name = html.escape(r["name"])
    desc = (r.get("description") or "").strip()
    if len(desc) > 62: desc = desc[:61].rstrip() + "…"
    desc = html.escape(desc, quote=False)
    lang = r.get("language") or "—"; col = LANG.get(lang, "#8b949e")
    stars = r.get("stargazers_count") or 0; forks = r.get("forks_count") or 0
    delay = i * 0.35
    b = f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.7s" fill="freeze"/>'
    b += f'<animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" begin="{delay:.2f}s" dur="0.7s" fill="freeze"/>'
    b += f'<text x="30" y="58" class="mono gr" font-size="38" font-weight="800" opacity=".95">{i+1:02d}</text>'
    b += f'<text x="104" y="44" class="mono t" font-size="22" font-weight="700">{name}</text>'
    # meta, laid out from the right edge
    x = 770
    parts = []
    if forks:
        parts.append(("fork", forks))
    parts.append(("star", stars)); parts.append(("lang", lang))
    for kind, val in parts:
        if kind == "fork":
            w = 16 + 8 * len(str(val)); x -= w
            b += (f'<g transform="translate({x},31)" fill="none" stroke="var(--d)" stroke-width="1.6"><circle cx="3" cy="3" r="2.4"/><circle cx="11" cy="3" r="2.4"/>'
                  f'<circle cx="7" cy="14" r="2.4"/><path d="M3 5.4v1.6a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V5.4M7 9v2.6"/></g>')
            b += f'<text x="{x+17}" y="43" class="d mono" font-size="14">{val}</text>'; x -= 18
        elif kind == "star":
            w = 16 + 8 * len(str(val)); x -= w
            b += f'<path transform="translate({x},30) scale(.62)" d="M10 0l3 6.8 7.4.7-5.6 5 1.7 7.3L10 15.9 3.5 19.8l1.7-7.3-5.6-5 7.4-.7z" fill="#f2c94c"/>'
            b += f'<text x="{x+16}" y="43" class="d mono" font-size="14">{val}</text>'; x -= 18
        else:
            w = 14 + 8.3 * len(val); x -= w
            b += f'<circle cx="{x+5}" cy="38" r="5.5" fill="{col}"/><text x="{x+16}" y="43" class="d mono" font-size="14">{html.escape(val)}</text>'
    if desc:
        b += f'<text x="770" y="78" text-anchor="end" class="t" font-size="17" opacity=".85">{desc}</text>'
    b += '<path d="M30 94H770" class="sp" fill="none"/>'
    b += (f'<rect y="92.5" width="90" height="2.4" rx="1.2" fill="url(#ln)"><animate attributeName="x" values="-90;800" dur="4s" '
          f'begin="{delay+1:.2f}s" repeatCount="indefinite"/></rect></g>')
    return svg(800, 104, b)

def main():
    data = load()
    repos = [r for r in data["repos"] if not r.get("fork") and r["name"].lower() != USER.lower()]
    repos.sort(key=lambda r: ((r.get("stargazers_count") or 0) + (r.get("forks_count") or 0), r.get("pushed_at") or ""), reverse=True)
    projects = repos[:MAX_PROJECTS]
    out = os.path.join(ROOT, "assets"); os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.startswith("project-"): os.remove(os.path.join(out, f))
    open(os.path.join(out, "stats.svg"), "w", encoding="utf-8").write(stats(data, projects))
    for i, r in enumerate(projects):
        open(os.path.join(out, f"project-{i+1}.svg"), "w", encoding="utf-8").write(project(i, r))
    # README projects block
    block = "\n".join(f'<a href="https://github.com/{USER}/{r["name"]}"><img src="assets/project-{i+1}.svg" width="82%" alt="{r["name"]}"/></a><br/>'
                      for i, r in enumerate(projects))
    p = os.path.join(ROOT, "README.md"); s = open(p, encoding="utf-8").read()
    a, b = "<!--PROJECTS:START-->", "<!--PROJECTS:END-->"
    if a in s and b in s:
        s = s[:s.index(a)+len(a)] + "\n" + block + "\n" + s[s.index(b):]
        open(p, "w", encoding="utf-8").write(s)
    print(f"{data['public_repos']} repos, {len(projects)} projects written")

if __name__ == "__main__":
    main()
