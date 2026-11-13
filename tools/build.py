import json, sys, os, datetime, html
sys.path.insert(0, os.path.dirname(__file__))
from content import PROJECTS, ORDER, GH

OUT = sys.argv[1]
REL = json.load(open(os.path.join(OUT, "data", "releases.json"), encoding="utf-8"))
P = {p["slug"]: p for p in PROJECTS}
ORDERED = [P[s] for s in ORDER]
POSTS = sorted(PROJECTS, key=lambda p: p["date"], reverse=True)

def fdate(d, short=False):
    if not d or d == "upcoming": return "Upcoming"
    x = datetime.date.fromisoformat(d)
    return x.strftime("%d %b %Y" if short else "%d %B %Y").lstrip("0")

def mb(n): return f"{n/1048576:.1f} MB" if n >= 1048576 else f"{n/1024:.0f} KB"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">'

SITE = "https://gaurav-gupta.co.in/"

def head(title, desc, root, extra="", path=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
<link rel="canonical" href="{SITE}{path}">
<script>if (location.protocol === "http:" && !/^(localhost|127[.]|192[.]168[.])/.test(location.hostname)) location.replace("https:" + location.href.substring(5));</script>
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<link rel="icon" href="{root}media/gg-logo.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="{root}css/classic.css">{extra}
</head>
<body>
"""

def masthead(root, active):
    items = [("Home", f"{root}index.html", "home"), ("About", f"{root}index.html#about", "about"),
             ("Projects", f"{root}index.html#projects", "projects"), ("Journal", f"{root}blog/index.html", "journal"),
             ("Downloads", f"{root}downloads.html", "downloads"), ("RDi 9.9", f"{root}rdi-9-9.html", "rdi"), ("Experience", f"{root}index.html#experience", "experience"),
             ("Meetings", f"{root}meetings.html", "meetings"), ("Community", f"{root}community.html", "community"),
             ("Contact", f"{root}index.html#contact", "contact")]
    lis = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' class="active"' if k == active else '', t) for t, h, k in items)
    return f"""<header class="masthead">
  <a class="monogram" href="{root}index.html" aria-label="Home">GG</a>
  <p class="name">Gaurav Gupta</p>
  <p class="motto">Software engineer · IBM i, Java &amp; developer tools · Salesforce</p>
  <hr class="double-rule">
</header>
<nav class="nav" aria-label="Main">
  <button class="nav-toggle" aria-label="Open menu">☰ Menu</button>
  <ul>{lis}</ul>
</nav>
"""

def footer(root):
    return f"""<footer class="footer">
  <div class="wrap">
    <span class="fleuron">❦</span>
    <p>&copy; 2026 Gaurav Gupta · Lucknow, Uttar Pradesh, India</p>
    <p><a href="https://github.com/gauravgupta0612">GitHub</a> · <a href="https://www.linkedin.com/in/gauravgupta865">LinkedIn</a> · <a href="https://www.salesforce.com/trailblazer/ggupta56">Trailblazer</a> · <a href="{root}downloads.html">Downloads</a></p>
    <p><img src="https://visitor-badge.laobi.icu/badge?page_id=gauravgupta0612.gaurav-portfolio" alt="Visitor count"></p>
  </div>
</footer>
"""

CHAT = """
<div id="chatbotWidget" class="chatbot-widget">
  <div class="chatbot-header"><div class="chatbot-title"><i class="fas fa-feather-pointed"></i> Ask about my work</div>
    <button class="chatbot-close" id="closeChatbot" aria-label="Close"><i class="fas fa-times"></i></button></div>
  <div class="chatbot-messages" id="chatbotMessages">
    <div class="message bot-message"><p>Hello! Ask me about Gaurav's projects, releases, skills or experience.</p></div>
  </div>
  <div class="chatbot-input-area">
    <input type="text" id="userInput" placeholder="Ask me anything…" class="chatbot-input">
    <button id="sendMessage" class="chatbot-send" aria-label="Send"><i class="fas fa-paper-plane"></i></button>
  </div>
</div>
<button id="chatbotToggle" class="chatbot-toggle" title="Open assistant"><i class="fas fa-comments"></i><span class="chatbot-badge">AI</span></button>
"""

def tail(root, chat=True):
    return (CHAT if chat else "") + f'<script src="{root}js/site.js"></script>\n</body>\n</html>\n'

def releases_for(p):
    return REL.get(p["release_key"] or "", [])

def project_links(p, root):
    out = [f'<a href="{root}blog/{p["slug"]}.html">Read the story</a>']
    if p.get("download"): out.append(f'<a href="{p["download"]}">⬇ {p["download_label"]}</a>')
    if p.get("repo"): out.append(f'<a href="{p["repo"]}">Source</a>')
    if p.get("docs"): out.append(f'<a href="{p["docs"]}">Docs</a>')
    if p.get("marketplace"): out.append(f'<a href="{p["marketplace"]}">Marketplace</a>')
    return " ".join(out)

ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X"]

# ---------------------------------------------------------------- index
def build_index():
    cards = []
    for i, p in enumerate(ORDERED):
        cards.append(f"""<article class="entry">
  <span class="no">No. {ROMAN[i]}</span>
  <h3><a href="blog/{p['slug']}.html">{html.escape(p['name'])}</a></h3>
  <div class="meta">Begun {fdate(p['date'])}<span class="badge-ver">v{p['latest']}</span></div>
  <p>{html.escape(p['tagline'])}</p>
  <div class="tags">{' · '.join(p['tags'])}</div>
  <p class="skills-used"><strong>Skills:</strong> {html.escape(p['skills'])}</p>
  <div class="links">{project_links(p, '')}</div>
</article>""")
    posts = "".join(f"""<li><time datetime="{p['date']}">{fdate(p['date'], True)}</time><div>
  <h3><a href="blog/{p['slug']}.html">{html.escape(p['blog_title'])}</a></h3>
  <p>{html.escape(p['dek'])} <span class="rt">· {p['read']} min read</span></p></div></li>""" for p in POSTS[:5])
    total_rel = sum(len(v) for v in REL.values())

    exp = [
      ("Dec 2025 – Present", "Senior Software Engineer", "ARCAD Software", "IBM i developer tooling: Eclipse plug-ins for IBM RDi 9.8 / 9.9, VS Code extensions, the Java 8 → 17 migration of server products, and AI / MCP integration. PMO across all ARCAD R&amp;D products."),
      ("Jul 2023 – Dec 2025", "Software Engineer", "ARCAD Software", "Java and Eclipse plug-ins for IBM Rational Developer for i, IBM i integration (RPG, CL, Db2 for i, IFS), OSGi / Tycho builds, GitHub and GitLab."),
      ("Oct 2022 – Jun 2025", "Freelancer", "Freelancer.com", "Salesforce development, Lightning components, Apex."),
      ("Nov 2021 – Jul 2022", "Salesforce Consultant", "Delhivery", "Sales Cloud, administration, Lightning, project management."),
      ("Oct 2020 – Sep 2021", "Salesforce Consultant", "C&amp;S Electric Ltd", "Apex, Lightning and cloud applications."),
      ("Apr 2020 – Oct 2020", "Salesforce Developer", "Kloudrac Inc", "Lightning, GitHub, Salesforce as a Service."),
      ("Jan 2020 – Apr 2020", "Intern – Salesforce", "Kcloud Technologies", "Salesforce CRM."),
    ]
    exp_html = "".join(f'<div class="cv-row"><div class="when">{w}</div><div><h3>{t}</h3><div class="org">{o}</div><p>{d}</p></div></div>' for w, t, o, d in exp)

    certs = [("Dive Deeper into GA4 Data and Reports", "Skillshop · Sep 2025"),
             ("OCI 2025 AI Foundations Associate", "Oracle · Sep 2025"),
             ("OCI 2025 Data Science Professional", "Oracle · Sep 2025"),
             ("IBM i Ready", "IBM · Sep 2025"),
             ("Build Smarter AI with Embeddings", "IBM · Sep 2025"),
             ("Artificial Intelligence Fundamentals", "IBM · Sep 2025"),
             ("Journey to Cloud: Envisioning Your Solution", "IBM · Sep 2025"),
             ("Copado Certified Developer & Administrator", "Copado · Apr 2021"),
             ("CCC – Course on Computer Concepts", "NIELIT India · Mar 2016")]
    certs_html = "".join(f"<li>{t}<span>{s}</span></li>" for t, s in certs)
    groups = [
      ("IBM i &amp; IBM Z", ["RPG IV / RPGLE (free and fixed form)", "CL programming &amp; commands", "DDS: PF, LF, DSPF, PRTF", "Db2 for i SQL &amp; QSYS2 services",
                          "IFS, PASE &amp; QSH", "Work management, journals &amp; security", "IBM Rational Developer for i (RDi 9.8 / 9.9)", "IBM i Debug Service &amp; ACS",
                          "z/OS: JCL, TSO, z/OSMF, PDS/PDSE, USS", "IBM i 7.4 – 7.6"]),
      ("Java &amp; Eclipse", ["Java 8 – 21", "Eclipse RCP, PDE &amp; OSGi plug-ins", "Tycho / Maven / p2 builds", "JDWP debugging"]),
      ("Developer tools &amp; web", ["VS Code extension API", "TypeScript, Node.js &amp; React", "Electron desktop apps", "Python"]),
      ("AI &amp; platforms", ["LLM integration &amp; routing", "Model Context Protocol (MCP)", "Agents with approval &amp; audit"]),
      ("Salesforce", ["Apex, Lightning, LWC, Aura", "Salesforce DX &amp; Copado", "Trailhead All Star Ranger"]),
      ("Delivery", ["GitHub, GitLab, Jenkins, Actions", "Release &amp; product management (PMO)", "Marketplace publishing"]),
    ]
    skills_html = "".join(f'<h3 class="skill-group">{g}</h3><ul class="skills-list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>" for g, items in groups)

    page = head("Gaurav Gupta — Software Engineer · Projects, Journal & Downloads",
                "Portfolio of Gaurav Gupta: Vanthrex for IBM i, Tavrion Studio, AI-Native Developer Platform and other developer tools, with release notes and downloads.", "", path="") + masthead("", "home") + f"""
<main>
<section id="about" class="wrap">
  <div class="intro">
    <figure class="portrait"><div class="frame"><img src="media/image (1).png" alt="Portrait of Gaurav Gupta"></div>
      <figcaption>Noida &amp; Lucknow, India</figcaption></figure>
    <div>
      <h2>I build the tools that take IBM i development, and the developers who do it, into the next decade.</h2>
      <p class="dropcap">For more than six years I have shipped software that real teams run every day: first enterprise CRM on Salesforce, then Java, Eclipse and VS Code tooling for IBM i at ARCAD Software, where I am a Senior Software Engineer and act as PMO for every R&amp;D product.</p>
      <p><strong>My mission is simple:</strong> no developer should have to choose between a platform that runs the business and tools that feel modern. IBM i, z/OS and Java systems hold some of the world's most important data, and the people who look after them deserve editors that check code as they type, debuggers that just work, AI that protects their secrets, and deployments they can undo with one command.</p>
      <p>Since 20 September 2026 I have designed, built and published <strong>{len(PROJECTS)} products and {total_rel} public releases</strong>, from Vanthrex, a complete IBM i workbench for VS Code, to Tavrion Studio, an Eclipse-ready IDE for Windows. Each has a story in the <a href="blog/index.html">Journal</a>, and every installer is on the <a href="downloads.html">Downloads</a> page.</p>
      <div class="facts">
        <div><strong>{len(PROJECTS)}</strong><span>new projects</span></div>
        <div><strong>{total_rel}</strong><span>public releases</span></div>
        <div><strong>6+</strong><span>years' experience</span></div>
      </div>
      <a class="btn primary" href="#projects">See the projects</a>
      <a class="btn" href="downloads.html">Downloads</a>
      <a class="btn" href="https://github.com/gauravgupta0612">GitHub</a>
    </div>
  </div>
</section>

<section id="projects" class="wrap">
  <div class="section-head"><div class="kicker">The Workshop</div><h2>Recent Projects</h2><div class="ornament">✦ ✦ ✦</div>
    <p>Everything I have built and released since 20 September 2026, newest first.</p></div>
  <div class="catalogue">{''.join(cards)}</div>
</section>

<section id="journal" class="narrow">
  <div class="section-head"><div class="kicker">From the Journal</div><h2>Latest Writing</h2><div class="ornament">✦ ✦ ✦</div></div>
  <ul class="journal-list">{posts}</ul>
  <p style="text-align:center;margin-top:22px"><a class="btn" href="blog/index.html">All journal entries</a></p>
</section>

<section id="experience" class="narrow">
  <div class="section-head"><div class="kicker">Curriculum Vitae</div><h2>Experience</h2><div class="ornament">✦ ✦ ✦</div></div>
  <div class="cv">{exp_html}</div>
</section>

<section id="certifications" class="wrap">
  <div class="two-col">
    <div><div class="section-head" style="text-align:left"><div class="kicker">Credentials</div><h2>Certifications</h2></div><ul class="certs">{certs_html}</ul></div>
    <div><div class="section-head" style="text-align:left"><div class="kicker">Craft</div><h2>Skills &amp; Education</h2></div>
      {skills_html}
      <ul class="certs" style="margin-top:22px"><li>MCA – Information Technology<span>Institute of Management Studies, Ghaziabad · 2018–2020</span></li>
      <li>BCA – Information Technology<span>Invertis University · 2015–2018</span></li>
      <li>Salesforce Trailhead All Star Ranger<span><a href="https://www.salesforce.com/trailblazer/ggupta56">213 badges · 83,875 points · 25 trails</a></span></li></ul>
    </div>
  </div>
</section>

<section id="contact" class="narrow contact">
  <div class="section-head"><div class="kicker">Correspondence</div><h2>Get in Touch</h2><div class="ornament">✦ ✦ ✦</div>
    <p>For questions about a project, a demo, or working together, write to me.</p></div>
  <div class="links">
    <a class="btn" href="mailto:ggupta865@gmail.com"><i class="fas fa-envelope"></i> Email</a>
    <a class="btn" href="https://www.linkedin.com/in/gauravgupta865"><i class="fab fa-linkedin"></i> LinkedIn</a>
    <a class="btn" href="https://github.com/gauravgupta0612"><i class="fab fa-github"></i> GitHub</a>
    <a class="btn" href="meetings.html"><i class="fas fa-calendar"></i> Book a meeting</a>
  </div>
</section>
</main>
""" + footer("") + tail("")
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)

# ---------------------------------------------------------------- blog
def release_block(p, root):
    rels = releases_for(p)
    parts = ['<h2>Release history</h2>']
    if p["history"]:
        lis = "".join(f'<li><span class="tv">v{v}</span> · <span class="td">{fdate(d)}</span><br>{t}</li>' for v, d, t in reversed(p["history"]))
        parts.append(f'<ul class="timeline">{lis}</ul>')
    elif rels:
        lis = "".join(f'<li><span class="tv">{r["name"]}</span> · <span class="td">{fdate(r["date"])}</span></li>' for r in rels)
        parts.append(f'<ul class="timeline">{lis}</ul>')
    if rels:
        latest = rels[0]
        assets = "".join(f'<li><a href="{a["url"]}">⬇ {html.escape(a["name"])}</a> <span class="size">({mb(a["size"])})</span></li>' for a in latest["assets"]) or f'<li><a href="{latest["url"]}">Release page</a></li>'
        parts.append(f'<div class="callout"><h4>Latest download: {html.escape(latest["name"])}</h4><ul>{assets}</ul><p>Every earlier version is on the <a href="{root}downloads.html#{p["slug"]}">Downloads page</a>.</p></div>')
    elif p.get("download"):
        parts.append(f'<div class="callout"><h4>Get it</h4><p><a href="{p["download"]}">{p["download_label"]}</a></p></div>')
    else:
        parts.append(f'<div class="callout"><h4>Get it</h4><p>{p["download_label"]}: <a href="{root}index.html#contact">contact me</a>.</p></div>')
    return "".join(parts)

def build_posts():
    os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)
    for i, p in enumerate(POSTS):
        newer = POSTS[i-1] if i > 0 else None
        older = POSTS[i+1] if i + 1 < len(POSTS) else None
        links = []
        if p.get("repo"): links.append(f'<a href="{p["repo"]}">Source on GitHub</a>')
        if p.get("docs"): links.append(f'<a href="{p["docs"]}">Documentation</a>')
        if p.get("marketplace"): links.append(f'<a href="{p["marketplace"]}">VS Code Marketplace</a>')
        nav = '<nav class="post-nav">' + \
            (f'<a href="{older["slug"]}.html"><small>← Earlier</small>{html.escape(older["blog_title"])}</a>' if older else "<span></span>") + \
            (f'<a href="{newer["slug"]}.html" style="text-align:right"><small>Later →</small>{html.escape(newer["blog_title"])}</a>' if newer else "<span></span>") + '</nav>'
        page = head(f'{p["blog_title"]} — Gaurav Gupta', p["dek"], "../", path=f'blog/{p["slug"]}.html') + masthead("../", "journal") + f"""
<main class="narrow">
<header class="article-head">
  <div class="kicker">The Journal · {html.escape(p['name'])}</div>
  <h1>{html.escape(p['blog_title'])}</h1>
  <p class="dek">{html.escape(p['dek'])}</p>
  <div class="byline">By Gaurav Gupta · <time datetime="{p['date']}">{fdate(p['date'])}</time> · {p['read']} min read · Latest v{p['latest']}</div>
</header>
<hr class="double-rule">
<article class="article">
{p['body']}
<h2>Skills applied</h2>
<p class="skills-used">{html.escape(p['skills'])}</p>
{release_block(p, '../')}
<p>{' · '.join(links)}</p>
</article>
{nav}
</main>
""" + footer("../") + tail("../")
        open(os.path.join(OUT, "blog", f'{p["slug"]}.html'), "w", encoding="utf-8").write(page)

    items = "".join(f"""<li><time datetime="{p['date']}">{fdate(p['date'], True)}</time><div>
  <h3><a href="{p['slug']}.html">{html.escape(p['blog_title'])}</a></h3>
  <p>{html.escape(p['dek'])} <span class="rt">· {html.escape(p['name'])} · {p['read']} min read</span></p></div></li>""" for p in POSTS)
    page = head("The Journal — Gaurav Gupta", "Stories behind each project, with release histories and downloads.", "../", path="blog/") + masthead("../", "journal") + f"""
<main class="narrow">
<section>
  <div class="section-head"><div class="kicker">The Journal</div><h2>Notes from the Workshop</h2><div class="ornament">✦ ✦ ✦</div>
    <p>One entry for each project begun since September 2026: why it exists, what it does, and how it has changed from release to release.</p></div>
  <ul class="journal-list">{items}</ul>
</section>
</main>
""" + footer("../") + tail("../")
    open(os.path.join(OUT, "blog", "index.html"), "w", encoding="utf-8").write(page)

# ---------------------------------------------------------------- downloads
def build_downloads():
    toc = "".join(f'<li><a href="#{p["slug"]}">{html.escape(p["name"])}</a> <span class="size">· v{p["latest"]}</span></li>' for p in ORDERED)
    tables = []
    for p in ORDERED:
        rels = releases_for(p)
        hist = {v: t for v, d, t in (p["history"] or [])}
        rows = []
        for j, r in enumerate(rels):
            v = r["tag"].split("-v")[-1].lstrip("v")
            note = hist.get(v, "")
            if p["slug"] == "devsuite": note = r["name"].rsplit(" v", 1)[0]
            assets = "".join(f'<a class="dl" href="{a["url"]}">⬇ {html.escape(a["name"])}</a> <span class="size">{mb(a["size"])}</span><br>' for a in r["assets"]) \
                     or f'<a class="dl" href="{r["url"]}">Release page</a>'
            rows.append('<tr' + (' class="latest"' if j == 0 else '') + f'><td class="v">{html.escape(r["tag"])}</td><td class="d">{fdate(r["date"], True)}</td><td>{note}</td><td>{assets}</td></tr>')
        # versions without a GitHub release asset (tags or local builds)
        released = {r["tag"].split("-v")[-1].lstrip("v") for r in rels}
        for v, d, t in reversed(p["history"] or []):
            if v in released: continue
            if d == "upcoming":
                where = "In development"
            elif p.get("repo") and p["slug"] == "vanthrex-for-ibm-i":
                where = f'<a href="{p["repo"]}/releases/tag/v{v}">Tag v{v}</a>'
            elif p["slug"] == "tavrion-studio":
                where = "Superseded by 1.4.0+"
            elif p.get("repo"):
                where = f'<a href="{p["repo"]}">Source</a>'
            else:
                where = "On request"
            rows.append(f'<tr><td class="v">v{v}</td><td class="d">{fdate(d, True)}</td><td>{t}</td><td>{where}</td></tr>')
        if p["slug"] == "ai-native-dev-platform":
            rows = [f'<tr class="latest"><td class="v">v0.2.0</td><td class="d">13 Nov 2026</td><td>First public version; npm package and JitPack build.</td><td><a href="{p["repo"]}/releases/tag/v0.2.0">Tag v0.2.0</a> · <a href="https://www.npmjs.com/package/@gauravgupta0612/ai-native-common">npm</a> · <a href="https://jitpack.io/#gauravgupta0612/ai-native-dev-platform">JitPack</a></td></tr>']
        if not rows:
            rows.append(f'<tr><td class="v">v{p["latest"]}</td><td class="d">{fdate(p["date"], True)}</td><td></td><td>{p["download_label"]}</td></tr>')
        extra = []
        if p.get("download"): extra.append(f'<a href="{p["download"]}">Latest</a>')
        if p.get("marketplace"): extra.append(f'<a href="{p["marketplace"]}">Marketplace</a>')
        if p.get("repo"): extra.append(f'<a href="{p["repo"]}/releases">All releases on GitHub</a>')
        tables.append(f"""<table class="ledger" id="{p['slug']}">
<caption>{html.escape(p['name'])}<small>{html.escape(p['tagline'])} — {' · '.join(extra) or 'available on request'} · <a href="blog/{p['slug']}.html">Read the story</a></small></caption>
<thead><tr><th>Version</th><th>Date</th><th>What changed</th><th>Files</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>""")
    page = head("Downloads & Release Notes — Gaurav Gupta", "Every release of Gaurav Gupta's projects: Windows installers (.exe), VS Code extensions (.vsix) and release notes.", "", path="downloads.html") + masthead("", "downloads") + f"""
<main class="wrap">
<section>
  <div class="section-head"><div class="kicker">The Ledger</div><h2>Downloads &amp; Release Notes</h2><div class="ornament">✦ ✦ ✦</div>
    <p>Every published release, with its installer or extension file. Windows <code>.exe</code> files install directly; <code>.vsix</code> files install in VS Code with <em>Extensions → … → Install from VSIX</em>.</p></div>
  <ul class="toc">{toc}</ul>
  {''.join(tables)}
  <p style="font-style:italic;color:var(--ink-soft)">Files are hosted on GitHub Releases. Last updated {fdate(datetime.date.today().isoformat())}.</p>
</section>
</main>
""" + footer("") + tail("")
    open(os.path.join(OUT, "downloads.html"), "w", encoding="utf-8").write(page)

from rdi import build_rdi
build_index(); build_posts(); build_downloads(); build_rdi(OUT, head, masthead, footer, tail)
print("built", len(POSTS), "posts")
