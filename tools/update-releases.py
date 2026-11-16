"""Refresh data/releases.json from GitHub Releases, then rebuild the site.

Usage (from the repository root):  python tools/update-releases.py
Add a new project to tools/content.py (PROJECTS + ORDER) and its repo to REPOS below.
"""
import json, os, re, subprocess, sys, urllib.request

OWNER = "gauravgupta0612"
REPOS = ["silverlake-ibmi", "tavrion-studio", "ai-native-dev-platform", "jatpilot",
         "Salesforce-DevPilot-Pack", "dataman-api-lens", "devsuite", "IBM-i-z-OS-Explorer"]
def summary(body):
    """First meaningful sentence of the release notes, as plain text."""
    for line in (body or "").splitlines():
        t = re.sub(r"[*_`#>]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", line).strip(" -:")
        if len(t) > 12 and not t.lower().startswith(("full changelog", "download", "what's changed")):
            return (t[:220] + "…") if len(t) > 220 else t
    return ""

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "portfolio-build"}
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]

out = {}
for repo in REPOS:
    url = f"https://api.github.com/repos/{OWNER}/{repo}/releases?per_page=100"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        rel = json.load(r)
    out[repo] = [{"tag": x["tag_name"], "date": x["published_at"][:10], "name": x["name"], "url": x["html_url"], "summary": summary(x.get("body")),
                  "assets": [{"name": a["name"], "url": a["browser_download_url"], "size": a["size"]} for a in x["assets"]]}
                 for x in rel if not x.get("draft")]
    print(f"{repo}: {len(out[repo])} releases")

def marketplace():
    """Install counts and ratings of every VS Code extension published by OWNER."""
    body = {"filters": [{"criteria": [{"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                                      {"filterType": 18, "value": OWNER}], "pageSize": 100}], "flags": 914}
    req = urllib.request.Request("https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "portfolio-build",
                                          "Accept": "application/json;api-version=7.2-preview.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        exts = json.load(r)["results"][0]["extensions"]
    rows = []
    for e in exts:
        st = {x["statisticName"]: x["value"] for x in e.get("statistics", [])}
        rows.append({"id": f'{e["publisher"]["publisherName"]}.{e["extensionName"]}', "name": e["displayName"],
                     "version": e["versions"][0]["version"], "installs": int(st.get("install", 0)),
                     "rating": round(st["averagerating"], 1) if st.get("ratingcount") else None,
                     "ratings": int(st["ratingcount"]) if st.get("ratingcount") else None})
    rows.sort(key=lambda x: -x["installs"])
    import datetime
    return {"checked": datetime.date.today().isoformat(), "extensions": rows}

try:
    stats = marketplace()
    with open(os.path.join(ROOT, "data", "marketplace.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=1)
    print("marketplace:", sum(x["installs"] for x in stats["extensions"]), "installs")
except Exception as e:
    print("marketplace stats not updated:", e)

with open(os.path.join(ROOT, "data", "releases.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py"), ROOT], check=True)
