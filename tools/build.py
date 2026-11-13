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

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'

SITE = "https://gaurav-gupta.co.in/"

def head(title, desc, root, extra="", path=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0b1020">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
<link rel="canonical" href="{SITE}{path}">
<script>if (location.protocol === "http:" && !/^(localhost|127[.]|192[.]168[.])/.test(location.hostname)) location.replace("https:" + location.href.substring(5));
try {{ var t = localStorage.getItem("gg-theme"); if (t) document.documentElement.setAttribute("data-theme", t); }} catch (e) {{}}</script>
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<link rel="icon" href="{root}media/gg-logo.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="{root}css/premium.css">{extra}
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<div class="bg-glow" aria-hidden="true"></div>
"""

def masthead(root, active):
    items = [("Home", f"{root}index.html", "home"), ("Projects", f"{root}index.html#projects", "projects"),
             ("Journal", f"{root}blog/index.html", "journal"), ("Downloads", f"{root}downloads.html", "downloads"),
             ("RDi 9.9", f"{root}rdi-9-9.html", "rdi"), ("Experience", f"{root}index.html#experience", "experience"),
             ("Meetings", f"{root}meetings.html", "meetings"), ("Community", f"{root}community.html", "community"),
             ("Contact", f"{root}index.html#contact", "contact")]
    lis = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' class="active" aria-current="page"' if k == active else '', t) for t, h, k in items)
    return f"""<header class="topbar">
  <div class="wrap topbar-in">
    <a class="brand" href="{root}index.html" aria-label="Gaurav Gupta, home"><span class="logo">GG</span><span class="brand-name">Gaurav Gupta</span></a>
    <nav class="nav" aria-label="Main"><ul>{lis}</ul></nav>
    <div class="top-actions">
      <button class="icon-btn theme-btn" aria-label="Switch light or dark theme" title="Light / dark"><i class="fas fa-circle-half-stroke"></i></button>
      <a class="btn primary sm hide-sm" href="{root}downloads.html"><i class="fas fa-download"></i> Downloads</a>
      <button class="icon-btn nav-toggle" aria-label="Open menu" aria-expanded="false"><i class="fas fa-bars"></i></button>
    </div>
  </div>
</header>
"""

def footer(root):
    return f"""<footer class="footer">
  <div class="wrap footer-grid">
    <div><a class="brand" href="{root}index.html"><span class="logo">GG</span><span class="brand-name">Gaurav Gupta</span></a>
      <p class="muted">Modern developer tools for IBM i, Java and AI. Built in Lucknow, India.</p></div>
    <div><h4>Explore</h4><a href="{root}index.html#projects">Projects</a><a href="{root}blog/index.html">Journal</a><a href="{root}downloads.html">Downloads</a><a href="{root}rdi-9-9.html">RDi 9.9 fix list</a></div>
    <div><h4>Connect</h4><a href="https://github.com/gauravgupta0612"><i class="fab fa-github"></i> GitHub</a><a href="https://www.linkedin.com/in/gauravgupta865"><i class="fab fa-linkedin"></i> LinkedIn</a><a href="https://www.salesforce.com/trailblazer/ggupta56"><i class="fas fa-star"></i> Trailblazer</a><a href="{root}meetings.html"><i class="fas fa-calendar"></i> Book a meeting</a></div>
  </div>
  <div class="wrap footer-bottom"><span>&copy; 2026 Gaurav Gupta</span><span class="secure"><i class="fas fa-lock"></i> Served over HTTPS</span><img src="https://visitor-badge.laobi.icu/badge?page_id=gauravgupta0612.gaurav-portfolio" alt="Visitor count" loading="lazy"></div>
</footer>
<button class="to-top" aria-label="Back to top"><i class="fas fa-arrow-up"></i></button>
"""

CHAT = """
<div id="chatbotWidget" class="chatbot-widget" role="dialog" aria-label="Assistant">
  <div class="chatbot-header"><div class="chatbot-title"><i class="fas fa-sparkles"></i> Ask about my work</div>
    <button class="chatbot-close" id="closeChatbot" aria-label="Close"><i class="fas fa-times"></i></button></div>
  <div class="chatbot-messages" id="chatbotMessages">
    <div class="message bot-message"><p>Hi! Ask me about Gaurav's projects, releases, IBM i skills or experience.</p></div>
  </div>
  <div class="chatbot-input-area">
    <input type="text" id="userInput" placeholder="Ask me anything…" class="chatbot-input" aria-label="Your question">
    <button id="sendMessage" class="chatbot-send" aria-label="Send"><i class="fas fa-paper-plane"></i></button>
  </div>
</div>
<button id="chatbotToggle" class="chatbot-toggle" title="Open assistant" aria-label="Open assistant"><i class="fas fa-comments"></i><span class="chatbot-badge">AI</span></button>
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
CATS = {"ai-native-dev-platform": ["ai", "java"], "tavrion-studio": ["java", "desktop"], "devflow": ["vscode"],
        "salesforce-devpilot-pack": ["vscode", "salesforce"], "jarpilot": ["ibmi"], "routinel": ["vscode"],
        "devsuite": ["vscode", "ibmi"], "ibm-i-zos-explorer": ["vscode", "ibmi"], "vanthrex-for-ibm-i": ["vscode", "ibmi", "ai"]}
FILTERS = [("all", "All"), ("ibmi", "IBM i / z"), ("vscode", "VS Code"), ("java", "Java & Eclipse"), ("ai", "AI"), ("desktop", "Desktop apps"), ("salesforce", "Salesforce")]
ICON = {"ai-native-dev-platform": "fa-brain", "tavrion-studio": "fa-laptop-code", "devflow": "fa-wave-square", "salesforce-devpilot-pack": "fa-cloud",
        "jarpilot": "fa-rocket", "routinel": "fa-route", "devsuite": "fa-layer-group", "ibm-i-zos-explorer": "fa-server", "vanthrex-for-ibm-i": "fa-terminal"}

def media(p, root):
    img = p.get("image")
    if img and p.get("image_kind") == "figure":
        return f'<div class="card-media"><img src="{root}media/projects/{img}" alt="{html.escape(p["name"])} screenshot" loading="lazy"></div>'
    inner = f'<img class="card-icon" src="{root}media/projects/{img}" alt="" loading="lazy">' if img else f'<i class="fas {ICON.get(p["slug"], "fa-cube")}"></i>'
    return f'<div class="card-media art art-{p["slug"]}">{inner}</div>'

def build_index():
    total_rel = sum(len(v) for v in REL.values())
    cards = []
    for p in ORDERED:
        btns = [f'<a class="btn ghost sm" href="blog/{p["slug"]}.html">Read story <i class="fas fa-arrow-right"></i></a>']
        if p.get("download"): btns.append(f'<a class="btn primary sm" href="{p["download"]}"><i class="fas fa-download"></i> Get it</a>')
        icons = []
        if p.get("repo"): icons.append(f'<a href="{p["repo"]}" aria-label="Source code"><i class="fab fa-github"></i></a>')
        if p.get("docs"): icons.append(f'<a href="{p["docs"]}" aria-label="Documentation"><i class="fas fa-book"></i></a>')
        if p.get("marketplace"): icons.append(f'<a href="{p["marketplace"]}" aria-label="VS Code Marketplace"><i class="fas fa-store"></i></a>')
        chips = "".join(f'<span class="chip">{t}</span>' for t in p["tags"])
        cards.append(f"""<article class="card project reveal" data-cats="{' '.join(CATS.get(p['slug'], []))}">
  {media(p, '')}
  <div class="card-body">
    <div class="card-top"><span class="ver">v{p['latest']}</span><span class="date">{fdate(p['date'], True)}</span></div>
    <h3><a href="blog/{p['slug']}.html">{html.escape(p['name'])}</a></h3>
    <p>{html.escape(p['tagline'])}</p>
    <div class="chips">{chips}</div>
    <details class="skills-more"><summary>Skills used</summary><p>{html.escape(p['skills'])}</p></details>
    <div class="card-actions">{''.join(btns)}<span class="icon-links">{''.join(icons)}</span></div>
  </div>
</article>""")
    filters = "".join(f'<button class="filter{" on" if k == "all" else ""}" data-filter="{k}">{t}</button>' for k, t in FILTERS)
    posts = "".join(f"""<a class="card post reveal" href="blog/{p['slug']}.html">
  <span class="post-meta">{fdate(p['date'], True)} · {p['read']} min read</span>
  <h3>{html.escape(p['blog_title'])}</h3><p>{html.escape(p['dek'])}</p><span class="more">Read <i class="fas fa-arrow-right"></i></span></a>""" for p in POSTS[:6])

    exp = [
      ("Dec 2025 – Present", "Senior Software Engineer", "ARCAD Software", "IBM i developer tooling: Eclipse plug-ins for IBM RDi 9.8 / 9.9, VS Code extensions, the Java 8 → 17 migration of server products, and AI / MCP integration. PMO across all ARCAD R&amp;D products."),
      ("Jul 2023 – Dec 2025", "Software Engineer", "ARCAD Software", "Java and Eclipse plug-ins for IBM Rational Developer for i, IBM i integration (RPG, CL, Db2 for i, IFS), OSGi / Tycho builds, GitHub and GitLab."),
      ("Oct 2022 – Jun 2025", "Freelancer", "Freelancer.com", "Salesforce development, Lightning components, Apex."),
      ("Nov 2021 – Jul 2022", "Salesforce Consultant", "Delhivery", "Sales Cloud, administration, Lightning, project management."),
      ("Oct 2020 – Sep 2021", "Salesforce Consultant", "C&amp;S Electric Ltd", "Apex, Lightning and cloud applications."),
      ("Apr 2020 – Oct 2020", "Salesforce Developer", "Kloudrac Inc", "Lightning, GitHub, Salesforce as a Service."),
      ("Jan 2020 – Apr 2020", "Intern – Salesforce", "Kcloud Technologies", "Salesforce CRM."),
    ]
    exp_html = "".join(f'<li class="reveal"><span class="when">{w}</span><h3>{t}</h3><span class="org">{o}</span><p>{d}</p></li>' for w, t, o, d in exp)

    groups = [
      ("fa-server", "IBM i &amp; IBM Z", ["RPG IV / RPGLE", "CL", "DDS (PF, LF, DSPF, PRTF)", "Db2 for i SQL", "QSYS2 services", "IFS · PASE · QSH",
                          "Work management &amp; security", "RDi 9.8 / 9.9", "IBM i Debug Service", "ACS", "z/OS JCL · TSO", "z/OSMF · USS", "IBM i 7.4 – 7.6"]),
      ("fa-mug-hot", "Java &amp; Eclipse", ["Java 8 – 21", "Eclipse RCP", "PDE &amp; OSGi", "Tycho · Maven · p2", "JDWP debugging"]),
      ("fa-code", "Developer tools &amp; web", ["VS Code extension API", "TypeScript", "Node.js", "React", "Electron", "Python"]),
      ("fa-brain", "AI &amp; platforms", ["LLM routing", "Model Context Protocol", "Agents with approval", "Secret &amp; PII masking"]),
      ("fa-cloud", "Salesforce", ["Apex", "Lightning · LWC · Aura", "Salesforce DX", "Copado", "Trailhead All Star Ranger"]),
      ("fa-diagram-project", "Delivery", ["GitHub · GitLab", "Jenkins · Actions", "Release management (PMO)", "Marketplace publishing"]),
    ]
    skills_html = "".join(f'<div class="card skill reveal"><div class="skill-head"><i class="fas {ic}"></i><h3>{g}</h3></div><div class="chips">' + "".join(f'<span class="chip">{x}</span>' for x in items) + "</div></div>" for ic, g, items in groups)

    certs = [("fa-ibm", "IBM i Ready", "IBM · Sep 2025"), ("fa-brain", "Build Smarter AI with Embeddings", "IBM · Sep 2025"),
             ("fa-robot", "Artificial Intelligence Fundamentals", "IBM · Sep 2025"), ("fa-cloud", "Journey to Cloud: Envisioning Your Solution", "IBM · Sep 2025"),
             ("fa-database", "OCI 2025 Data Science Professional", "Oracle · Sep 2025"), ("fa-microchip", "OCI 2025 AI Foundations Associate", "Oracle · Sep 2025"),
             ("fa-chart-line", "Dive Deeper into GA4 Data and Reports", "Skillshop · Sep 2025"), ("fa-code-branch", "Copado Certified Developer &amp; Administrator", "Copado · Apr 2021"),
             ("fa-graduation-cap", "MCA – Information Technology", "IMS Ghaziabad · 2018–2020"), ("fa-graduation-cap", "BCA – Information Technology", "Invertis University · 2015–2018")]
    certs_html = "".join(f'<div class="cert reveal"><i class="fas {ic if ic != "fa-ibm" else "fa-award"}"></i><div><strong>{t}</strong><span>{s}</span></div></div>' for ic, t, s in certs)
    marquee_items = ["IBM i", "RPGLE", "CL", "Db2 for i", "RDi 9.9", "z/OS", "Java 21", "Eclipse / OSGi", "VS Code", "TypeScript", "Electron", "LLMs", "MCP", "Salesforce", "GitHub Actions"]
    marquee = "".join(f"<span>{m}</span>" for m in marquee_items * 2)
    vrel = len(REL.get("silverlake-ibmi", []))

    page = head("Gaurav Gupta — Developer tools for IBM i, Java & AI",
                "Gaurav Gupta builds modern developer tools for IBM i, Java and AI: Vanthrex for IBM i, Tavrion Studio, the AI-Native Developer Platform and more, with release notes and downloads.", "", path="") + masthead("", "home") + f"""
<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="pill"><span class="dot"></span> Senior Software Engineer · ARCAD Software · 6+ years</span>
      <h1>I build the tools that bring <span class="grad">IBM i, Java &amp; AI</span> development into the next decade.</h1>
      <p class="lead">IBM i, z/OS and Java systems run some of the world's most important businesses. The developers who look after them deserve editors that check code as they type, debuggers that just work, AI that protects their secrets, and deployments they can undo with one command. That is what I build.</p>
      <div class="cta">
        <a class="btn primary lg" href="#projects"><i class="fas fa-cubes"></i> Explore projects</a>
        <a class="btn ghost lg" href="downloads.html"><i class="fas fa-download"></i> Downloads</a>
        <a class="btn ghost lg icon-only" href="https://github.com/gauravgupta0612" aria-label="GitHub"><i class="fab fa-github"></i></a>
      </div>
      <dl class="stats">
        <div><dt data-count="{len(PROJECTS)}">{len(PROJECTS)}</dt><dd>products since Sep 2026</dd></div>
        <div><dt data-count="{total_rel}">{total_rel}</dt><dd>public releases</dd></div>
        <div><dt data-count="6" data-suffix="+">6+</dt><dd>years shipping software</dd></div>
        <div><dt data-count="213">213</dt><dd>Trailhead badges</dd></div>
      </dl>
    </div>
    <div class="hero-visual">
      <div class="orbit"><div class="photo"><img src="media/image (1).png" alt="Gaurav Gupta"></div></div>
      <a class="float f1" href="blog/vanthrex-for-ibm-i.html"><i class="fas fa-terminal"></i><div><strong>Vanthrex for IBM i</strong><span>v3.2.1 · {vrel} releases on GitHub</span></div></a>
      <a class="float f2" href="blog/tavrion-studio.html"><i class="fas fa-laptop-code"></i><div><strong>Tavrion Studio</strong><span>Windows .exe · v1.5.0</span></div></a>
      <a class="float f3" href="rdi-9-9.html"><i class="fas fa-list-check"></i><div><strong>RDi 9.9 fix list</strong><span>Current: 9.9.0.8</span></div></a>
    </div>
  </div>
  <div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>
</section>

<section id="projects" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Projects</span><h2>Products I've shipped since 20 September 2026</h2>
      <p>Nine tools, each with a story, a release history and a download. Filter by the area you care about.</p></div>
    <div class="filters" role="group" aria-label="Filter projects">{filters}</div>
    <div class="grid projects-grid">{''.join(cards)}</div>
  </div>
</section>

<section class="section spotlight">
  <div class="wrap spot-grid">
    <div class="reveal">
      <span class="eyebrow">Flagship</span>
      <h2>Vanthrex for IBM i</h2>
      <p class="lead">A complete IBM i workbench for VS Code: more than 50 RPG, CL, SQL and DDS checks as you type, one-click quick fixes, debugging, a System Tracker, GO menus for AS/400 veterans, and an AI assistant that never sees your secrets.</p>
      <ul class="ticks"><li>About 30 releases in five weeks</li><li>Translated into 5 languages</li><li>Production-safe connections with Read-only mode</li><li>One-step import from Code for IBM i</li></ul>
      <div class="cta"><a class="btn primary" href="https://marketplace.visualstudio.com/items?itemName=gauravgupta0612.vanthrex-ibmi"><i class="fas fa-store"></i> VS Code Marketplace</a><a class="btn ghost" href="blog/vanthrex-for-ibm-i.html">Read the story</a></div>
    </div>
    <div class="spot-shot reveal"><div class="window"><div class="window-bar"><span></span><span></span><span></span></div><img src="media/projects/vanthrex-toolbox.png" alt="Vanthrex Developer Toolbox in VS Code" loading="lazy"></div></div>
  </div>
</section>

<section id="journal" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Journal</span><h2>Stories behind the releases</h2>
      <p>Why each tool exists, what it does, and how it changed from version to version.</p></div>
    <div class="grid posts-grid">{posts}</div>
    <div class="center"><a class="btn ghost" href="blog/index.html">All journal entries <i class="fas fa-arrow-right"></i></a></div>
  </div>
</section>

<section id="skills" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Skills</span><h2>From RPG to LLMs</h2>
      <p>Deep IBM i and Java roots, with modern tooling, AI and Salesforce on top.</p></div>
    <div class="grid skills-grid">{skills_html}</div>
  </div>
</section>

<section id="experience" class="section">
  <div class="wrap exp-grid">
    <div class="reveal"><span class="eyebrow">Experience</span><h2>6+ years of shipping software</h2>
      <p class="muted">From Salesforce consulting to IBM i developer tools, always close to the people who use what I build.</p>
      <a class="trail card" href="https://www.salesforce.com/trailblazer/ggupta56"><i class="fas fa-trophy"></i><div><strong>Trailhead All Star Ranger</strong><span>213 badges · 83,875 points · 25 trails</span></div></a></div>
    <ol class="xp">{exp_html}</ol>
  </div>
</section>

<section id="certifications" class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Credentials</span><h2>Certifications &amp; education</h2></div>
    <div class="grid certs-grid">{certs_html}</div>
  </div>
</section>

<section id="contact" class="section">
  <div class="wrap">
    <div class="cta-band reveal">
      <div><h2>Let's build something developers love.</h2><p>Questions about a tool, a demo for your team, or working together. I usually reply within a day.</p></div>
      <div class="cta">
        <a class="btn light" href="mailto:ggupta865@gmail.com"><i class="fas fa-envelope"></i> Email me</a>
        <a class="btn outline-light" href="https://www.linkedin.com/in/gauravgupta865"><i class="fab fa-linkedin"></i> LinkedIn</a>
        <a class="btn outline-light" href="meetings.html"><i class="fas fa-calendar"></i> Book a meeting</a>
      </div>
    </div>
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
  <span class="eyebrow">The Journal · {html.escape(p['name'])}</span>
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

    items = "".join(f"""<a class="card post reveal" href="{p['slug']}.html">
  <span class="post-meta">{fdate(p['date'], True)} · {html.escape(p['name'])} · {p['read']} min read</span>
  <h3>{html.escape(p['blog_title'])}</h3><p>{html.escape(p['dek'])}</p><span class="more">Read <i class="fas fa-arrow-right"></i></span></a>""" for p in POSTS)
    page = head("The Journal — Gaurav Gupta", "Stories behind each project, with release histories and downloads.", "../", path="blog/") + masthead("../", "journal") + f"""
<main class="wrap">
<section class="section">
  <div class="section-head"><span class="eyebrow">The Journal</span><h2>Stories behind the releases</h2>
    <p>One entry for each project begun since September 2026: why it exists, what it does, and how it has changed from release to release.</p></div>
  <div class="grid posts-grid">{items}</div>
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
<section class="section">
  <div class="section-head"><span class="eyebrow">Downloads</span><h2>Downloads &amp; Release Notes</h2>
    <p>Every published release, with its installer or extension file. Windows <code>.exe</code> files install directly; <code>.vsix</code> files install in VS Code with <em>Extensions → … → Install from VSIX</em>.</p></div>
  <div class="search"><i class="fas fa-magnifying-glass"></i><input type="search" id="dlSearch" placeholder="Search releases, versions or file names…" aria-label="Search releases"></div>
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
