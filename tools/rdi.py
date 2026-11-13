"""IBM Rational Developer for i 9.9 — fix pack list page (data from IBM's public fix list)."""
import os

FIXLIST = "https://www.ibm.com/support/pages/fix-list-rational-developer-i"
DOCS = "https://www.ibm.com/docs/en/rdfi/9.9.0?topic=installing-update-product-newer-version"
HUB = "https://www.ibm.com/support/pages/ibm-rational-developer-i-hub"

def fc(v):
    return ("https://www.ibm.com/support/fixcentral/swg/quickorder?parent=ibm%7ERational&product=ibm/Rational/Rational+Developer+for+i"
            f"&release={v}&platform=All&function=fixId&fixids={v}-Rational-RDI-fp&includeRequisites=0&includeSupersedes=0&downloadMethod=http&source=fc")

RDI99 = [
 ("9.9.0.8", "FP8", "23 Oct 2026", True,  "Security updates."),
 ("9.9.0.7", "FP7", "25 Sep 2026", False, "Security updates."),
 ("9.9.0.6", "FP6", "14 Sep 2026", False, "Security updates."),
 ("9.9.0.5", "FP5", "14 Aug 2026", False, "Fixes DT498064 (Verify hangs on RPGLE source with an include), DT496537 (SQL syntax checking in the RSE LPEX editor) and DT461201 (CL line-length reformatting). New CL and DDS templates (idea IBMI-I-3347)."),
 ("9.9.0.4", "FP4", "9 Jul 2026",  False, "<strong>Multi-factor authentication support.</strong> Fixes DT473932 (garbled characters in the Error List), SE79811 and SE80804 (macOS editor issues) and DT474633 (progress dialog steals focus)."),
 ("9.9.0.3", "FP3", "5 Jun 2026",  False, "Partial fix for DT468024 (i Projects Navigator). Fixes SE80855 (remote reconciler with eGit shows false conflicts), DT463080 (crash on Source Validate/Verify) and DT461825 (NL characters in program verifiers)."),
 ("9.9.0.2", "FP2", "24 Apr 2026", False, "IBM Java updated to 21.0.10.1. Fixes DT462072 (default template not applied to new members), DT455184 (debug fails with SSH secure communications) and SE81352 (Japanese IME input on macOS)."),
 ("9.9.0.1", "FP1", "6 Feb 2026",  False, "Security updates."),
 ("9.9",     "GA",  "27 Jan 2026", False, "General availability: Eclipse base 4.31, IBM Java 21.0.9, RPG and COBOL language updates, eGit 7.3. ACS is no longer bundled. Known issue: i Projects Navigator view missing (DT468024)."),
]
RDI98 = [("9.8.0.8","FP8","1 Apr 2026"),("9.8.0.7","FP7","27 Feb 2026"),("9.8.0.6","FP6","8 Sep 2025"),("9.8.0.5","FP5","2 Jun 2025"),
         ("9.8.0.4","FP4","6 Mar 2025"),("9.8.0.3","FP3","3 Dec 2024"),("9.8.0.2","FP2","6 Jun 2024"),("9.8.0.1","FP1","8 Jan 2024"),("9.8","GA","28 Apr 2023")]

def build_rdi(out, head, masthead, footer, tail):
    rows = []
    for v, fp, d, cur, notes in RDI99:
        dl = f'<a class="dl" href="{fc(v)}">Fix Central ⬇</a>' if fp != "GA" else f'<a class="dl" href="{HUB}">RDi hub</a>'
        status = '<strong style="color:var(--accent)">Current</strong>' if cur else "Superseded"
        cls = ' class="latest"' if cur else ''
        rows.append(f'<tr{cls}><td class="v">{v}<br><span class="size">{fp}</span></td><td class="d">{d}</td><td>{status}</td><td>{notes}</td><td>{dl}</td></tr>')
    rows98 = "".join(('<tr class="latest">' if i == 0 else '<tr>') + f'<td class="v">{v}</td><td>{fp}</td><td class="d">{d}</td><td>{"Current 9.8 level" if i == 0 else "Superseded"}</td><td>' +
                     (f'<a class="dl" href="{fc(v)}">Fix Central ⬇</a>' if fp != "GA" else "—") + "</td></tr>" for i, (v, fp, d) in enumerate(RDI98))
    page = head("IBM RDi 9.9 Fix Pack List — every version | Gaurav Gupta",
                "IBM Rational Developer for i 9.9: every fix pack from GA to 9.9.0.8 with dates, APAR fixes and download links, plus the 9.8 fix pack history.",
                "", path="rdi-9-9.html") + masthead("", "rdi") + f"""
<main class="wrap">
<section class="section">
  <div class="section-head"><span class="eyebrow">Reference · IBM i</span><h2>IBM Rational Developer for i 9.9</h2>
    <p>Every 9.9 version and fix pack in one place, with release dates, what each one fixed, and where to download it. Current level: <strong>9.9.0.8 (FP8)</strong>.</p></div>

  <div class="narrow" style="padding:0">
  <div class="callout"><h4>What changed in 9.9</h4>
    <ul>
      <li><strong>New platform:</strong> Eclipse 4.31 base and IBM Java 21 (21.0.10.1 from FP2), with eGit 7.3.</li>
      <li><strong>Languages:</strong> RPG and COBOL language updates; new CL and DDS templates in FP5.</li>
      <li><strong>Security:</strong> multi-factor authentication from FP4, and security updates in FP1, FP6, FP7 and FP8.</li>
      <li><strong>Install:</strong> IBM Access Client Solutions (ACS) is no longer bundled with 9.9. Install and update through IBM Installation Manager; see IBM&#39;s <a href="{DOCS}">update guide</a>.</li>
    </ul>
    <p>For plug-in developers, the move to Eclipse 4.31 and Java 21 usually means updating the target platform, bundle version ranges and <code>Import-Package</code> entries, and running regression tests on 9.9 before shipping.</p>
  </div>
  </div>

  <table class="ledger" id="rdi99">
    <caption>RDi 9.9 fix packs<small>Newest first. Download links open IBM Fix Central (IBM ID required). Install guide: <a href="{DOCS}">Update to a newer version</a>.</small></caption>
    <thead><tr><th>Version</th><th>Released</th><th>Status</th><th>Fixes &amp; changes</th><th>Download</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>

  <table class="ledger" id="rdi98">
    <caption>RDi 9.8 fix packs, for reference<small>The latest 9.8 fix pack is 9.8.0.8 (1 April 2026).</small></caption>
    <thead><tr><th>Version</th><th>Fix pack</th><th>Released</th><th>Status</th><th>Download</th></tr></thead>
    <tbody>{rows98}</tbody>
  </table>

  <p style="font-style:italic;color:var(--ink-soft)">Source: IBM, <a href="{FIXLIST}">Fix list for Rational Developer for i</a> (checked 13 November 2026). APAR descriptions are summarised; IBM's fix list is the authoritative reference.</p>
</section>
</main>
""" + footer("") + tail("")
    open(os.path.join(out, "rdi-9-9.html"), "w", encoding="utf-8").write(page)
