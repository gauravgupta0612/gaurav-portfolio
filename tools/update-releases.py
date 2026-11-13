"""Refresh data/releases.json from GitHub Releases, then rebuild the site.

Usage (from the repository root):  python tools/update-releases.py
Add a new project to tools/content.py (PROJECTS + ORDER) and its repo to REPOS below.
"""
import json, os, subprocess, sys, urllib.request

OWNER = "gauravgupta0612"
REPOS = ["silverlake-ibmi", "tavrion-studio", "ai-native-dev-platform", "jatpilot",
         "Salesforce-DevPilot-Pack", "dataman-api-lens", "devsuite", "IBM-i-z-OS-Explorer"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

out = {}
for repo in REPOS:
    url = f"https://api.github.com/repos/{OWNER}/{repo}/releases?per_page=100"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "portfolio-build"})
    with urllib.request.urlopen(req, timeout=30) as r:
        rel = json.load(r)
    out[repo] = [{"tag": x["tag_name"], "date": x["published_at"][:10], "name": x["name"], "url": x["html_url"],
                  "assets": [{"name": a["name"], "url": a["browser_download_url"], "size": a["size"]} for a in x["assets"]]}
                 for x in rel if not x.get("draft")]
    print(f"{repo}: {len(out[repo])} releases")

with open(os.path.join(ROOT, "data", "releases.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py"), ROOT], check=True)
