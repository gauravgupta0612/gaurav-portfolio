# Content for the portfolio: projects created since 20 Sep 2026, blog posts and release notes.
GH = "https://github.com/gauravgupta0612"

PROJECTS = [
 {
  "slug": "tavrion-studio", "skills": "Electron, Node.js, Java (javac, JDWP/jdb debugger), Eclipse JDT & PDE model, OSGi (Equinox/Felix), p2 & Maven resolution, Monaco editor, Windows installer (NSIS)", "name": "Tavrion Studio", "date": "2026-11-12",
  "tagline": "A VS Code-style IDE that opens, builds, runs and debugs Eclipse Java projects.",
  "tags": ["Electron", "Java", "Eclipse / OSGi", "Monaco"],
  "repo": f"{GH}/tavrion-studio", "release_key": "tavrion-studio",
  "latest": "1.5.0", "download": f"{GH}/tavrion-studio/releases/latest", "download_label": "Windows installer (.exe)",
  "image": "tavrion-icon.png", "image_kind": "icon",
  "blog_title": "Tavrion Studio: an IDE that speaks Eclipse",
  "dek": "Why I built a lightweight, VS Code-style IDE for Eclipse workspaces, and what ships in the Windows installer.",
  "read": 7,
  "body": """
<p>Eclipse is still where much of the enterprise Java world lives, with plug-in projects, <code>.target</code> platforms and carefully tuned launch configurations. VS Code feels lighter and faster, but it has never quite understood an Eclipse workspace. Tavrion Studio is my attempt to have both: the editor experience of VS Code with an engine that reads Eclipse projects the way Eclipse does.</p>
<p>The project began on 12 November 2026 under the working name <em>Nexora Studio</em>. Four builds (1.0 to 1.3) went out under that name the same day. To avoid any naming conflicts, it was renamed <strong>Tavrion Studio</strong> for version 1.4, and the source moved to its own public repository.</p>
<h2>What it does</h2>
<ul>
<li><strong>Eclipse compatibility.</strong> Reads <code>.project</code>, <code>.classpath</code> and JDT compliance settings, builds dependent projects first in Eclipse order, and imports and exports Eclipse <code>.launch</code> files.</li>
<li><strong>Run and debug.</strong> Launch configurations live in <code>.tavrion/launch.json</code>. The debugger is built on JDWP and jdb and supports conditional breakpoints, hit counts, logpoints, Run to Line, watch expressions, a call stack and hover-to-inspect values.</li>
<li><strong>Java editing on Monaco.</strong> Eclipse templates (<code>sysout</code>, <code>main</code>, <code>foreach</code>…), auto-import, Organize Imports, Outline, Go to Definition and Open Type, with javac errors shown inline.</li>
<li><strong>PDE and OSGi.</strong> Set a <code>.target</code> file as the target platform. Bundles come from local p2 and Maven caches first, then from the p2 repositories, and Equinox or Felix launches start with the Gogo shell.</li>
<li><strong>Developer Toolbox.</strong> Environment Doctor, a TODO/FIXME finder, Ports and Processes, and a REST client, all one shortcut away.</li>
<li><strong>Beyond Java.</strong> It also opens TypeScript, React, React Native/Expo, Python, Go, Rust, C/C++ and .NET projects.</li>
</ul>
<h2>Download</h2>
<p>Tavrion Studio ships as two Windows executables on every release: <em>Setup</em> (Start menu and desktop shortcuts, with a choice of install folder) and <em>Portable</em> (no installation needed). It needs a JDK, version 8 or later; 11, 17 or 21 is recommended.</p>
<div class="callout"><h4>Note on Windows SmartScreen</h4><p>The executables are not code-signed yet, so Windows may show a warning. Choose <em>More info → Run anyway</em>.</p></div>
""",
  "history": [
    ("1.0.0 – 1.3.0", "2026-11-12", "Built as <em>Nexora Studio</em>: Eclipse model, build, run and debug engine, and the Windows installer."),
    ("1.4.0", "2026-11-13", "Renamed <strong>Tavrion Studio</strong>; first public release with Setup and Portable .exe files."),
    ("1.5.0", "2026-11-13", "Current release; Setup and Portable .exe files on GitHub Releases."),
  ],
 },
 {
  "slug": "ai-native-dev-platform", "skills": "TypeScript, Java 17, Python, LLM routing (OpenAI, Claude, Gemini, Ollama), agent design, MCP, code indexing (incl. IBM i RPG), security & audit controls, CI/CD, npm & JitPack publishing", "name": "AI-Native Developer Platform", "date": "2026-11-13",
  "tagline": "A security-first platform for building AI developer tools: multi-model routing, safe agents, code intelligence and enterprise controls.",
  "tags": ["TypeScript", "Java", "Python", "LLM", "MCP"],
  "repo": f"{GH}/ai-native-dev-platform", "release_key": "ai-native-dev-platform",
  "latest": "0.2.0", "download": f"{GH}/ai-native-dev-platform", "download_label": "Source & packages",
  "image": "ai-platform-architecture.png", "image_kind": "figure",
  "blog_title": "Designing an AI-native developer platform",
  "dek": "One API for every model, agents that ask before they act, and your secrets kept on your machine.",
  "read": 6,
  "body": """
<p>Most AI coding tools tie you to one model, send your code wherever they like, and give you very little control. I wanted the opposite: a platform where the organisation decides which model sees what, where agents can explore freely but cannot change anything without approval, and where the whole thing can be audited.</p>
<p>The AI-Native Developer Platform grew out of a "NextGen AI IDE" architecture I sketched earlier this year. The first public version went up on GitHub on 13 November 2026 and is tagged <code>v0.2.0</code>.</p>
<figure><img src="../media/projects/ai-platform-architecture.png" alt="AI-Native Developer Platform architecture overview"><figcaption>Architecture overview: router, agents, tools, knowledge layer and enterprise controls.</figcaption></figure>
<h2>Principles</h2>
<ul>
<li><strong>Any model, one API.</strong> OpenAI, Anthropic Claude, Google Gemini, local Ollama models or your own gateway, with per-task routing, retry and fallback.</li>
<li><strong>Your data stays yours.</strong> Prompts that contain card numbers, phone numbers, keys or other sensitive data stay on the local model automatically, and secrets are masked before anything leaves the machine.</li>
<li><strong>Agents that are safe to run.</strong> Agents can read, search and analyse code on their own. Writing files and running commands always require approval, and budgets stop runaway loops and costs.</li>
<li><strong>Understands the code base.</strong> Semantic search, a symbol index (TypeScript, Java, Python and IBM i RPG) and a knowledge graph that answers "what breaks if I change this?".</li>
<li><strong>Enterprise-ready.</strong> Layered policies, a tamper-evident audit log, an encrypted key vault, signed extensions, cost reports and an air-gapped mode.</li>
<li><strong>Zero runtime dependencies.</strong> The shared library exists in TypeScript, Java and Python and uses only each language's standard library.</li>
</ul>
<h2>Try it</h2>
<p>You need Node.js 22+ and git: clone the repository, run <code>npm install</code> and <code>npm test</code>, then <code>npm start -- /path/to/project</code> to open the interactive AI shell. With no API key it falls back to a local Ollama model, or to an offline echo model, so you can explore every feature first.</p>
""",
  "history": [("0.2.0", "2026-11-13", "First public version on GitHub; CI, npm package and JitPack build.")],
 },
 {
  "slug": "vanthrex-for-ibm-i", "skills": "IBM i (RPGLE, CL, DDS, Db2 for i SQL, IFS, PASE), SSH & Mapepire, IBM i Debug Service, QSYS2 services, work management & security (*SECADM), VS Code API, TypeScript, i18n, Marketplace publishing", "name": "Vanthrex for IBM i", "date": "2026-10-03",
  "tagline": "An all-in-one IBM i workbench for VS Code: connect, edit, compile, SQL, code checks, debugging and system tools.",
  "tags": ["VS Code", "TypeScript", "IBM i", "RPG / CL / SQL"],
  "repo": f"{GH}/silverlake-ibmi", "release_key": "silverlake-ibmi",
  "docs": "https://gauravgupta0612.github.io/vanthrex-ibmi-docs/",
  "marketplace": "https://marketplace.visualstudio.com/items?itemName=gauravgupta0612.vanthrex-ibmi",
  "latest": "3.2.1", "download": f"{GH}/silverlake-ibmi/releases/latest", "download_label": "VS Code extension (.vsix)",
  "image": "vanthrex-rpg-checks.png", "image_kind": "figure",
  "blog_title": "Vanthrex for IBM i: thirty releases in five weeks",
  "dek": "How a weekend VS Code experiment became a full IBM i workbench, release by release.",
  "read": 11,
  "body": """
<p>IBM i developers deserve tools that are as pleasant as the ones the rest of the industry takes for granted. Vanthrex started on 3 October 2026 as <em>Silverlake for IBM i</em>, a small VS Code extension to browse libraries and edit source members. Five weeks and about thirty releases later, it is an all-in-one workbench that covers the whole working day of an RPG, CL and SQL developer.</p>
<figure><img src="../media/projects/vanthrex-rpg-checks.png" alt="RPG checks in the editor and the Problems view"><figcaption>More than 50 checks for RPG, CL and SQL while you type, shown in <em>Problems</em>.</figcaption></figure>
<h2>The idea</h2>
<p>Install, add a connection, open a member, press <kbd>Ctrl+S</kbd> and <kbd>Ctrl+Alt+C</kbd>. Everything else should be discoverable from one shortcut (<kbd>Ctrl+Alt+A</kbd>) that shows the tools that fit the file you are in. If you are coming from Code for IBM i, <em>Import My Code for IBM i Setup…</em> brings your connections, library lists and compile actions over in one step.</p>
<h2>Highlights</h2>
<ul>
<li><strong>Editing:</strong> SEU-style source dates, RPG semantic highlighting, DDS and CL checks, a CL formatter, fixed-to-free conversion and quick fixes.</li>
<li><strong>Understanding code:</strong> call graphs, "who calls each exported procedure", flowcharts, DSPF screen preview and database diagrams.</li>
<li><strong>Running safely:</strong> Production and Read-only connection modes, a self-check, and error messages that tell you what to do next.</li>
<li><strong>System insight:</strong> System Tracker, performance monitor, Library Space Map, Batch Job Timeline, Index Advisor and journal explorer.</li>
<li><strong>AI with guard rails:</strong> the <code>@vanthrex</code> chat participant only reads, and secrets, personal data and sensitive columns are masked before anything reaches a model.</li>
<li><strong>AS/400 at heart:</strong> GO menus, PDM-style lists and green-screen commands for people who grew up on a 5250.</li>
</ul>
<figure><img src="../media/projects/vanthrex-quick-fix.png" alt="Quick fix adding an IF NOT %FOUND test after CHAIN"><figcaption>Quick fixes: <kbd>Ctrl+.</kbd> on a warning adds the missing code.</figcaption></figure>
<h2>Install</h2>
<p>Install it from the VS Code Marketplace (<code>code --install-extension gauravgupta0612.vanthrex-ibmi</code>), or download the <code>.vsix</code> from GitHub Releases and use <em>Extensions → … → Install from VSIX</em>. Full documentation is on the <a href="https://gauravgupta0612.github.io/vanthrex-ibmi-docs/">Vanthrex documentation site</a>.</p>
""",
  "history": [
    ("0.1.0", "2026-10-03", "First release as <em>Silverlake</em>: guided connection, libraries & source browser, quick-action menu."),
    ("0.2.0", "2026-10-03", "System dashboard, Active Jobs and Messages views."),
    ("0.3.0", "2026-10-03", "Renamed <strong>Vanthrex for IBM i</strong>; first Marketplace release; SEU-style source dates."),
    ("0.3.1", "2026-10-04", "Documentation site goes online."),
    ("0.4.0", "2026-10-03", "Object information page; members always open with the Mapepire SQL engine."),
    ("0.5.0", "2026-10-03", "Debug Program: full VS Code debug sessions through the IBM i Debug Service."),
    ("0.6.0", "2026-10-05", "<code>@vanthrex</code> chat assistant: /explain, /document, /review, /modernize; read-only by design."),
    ("0.6.1", "2026-10-05", "Stable (no longer Preview) on the Marketplace; automated publishing."),
    ("0.7.0", "2026-10-09", "Who calls each exported procedure of a service program."),
    ("0.7.1", "2026-10-10", "Run SQL Query from anywhere, with a sortable result grid."),
    ("0.8.0", "2026-10-11", "Index Advisor, compare table data DEV ↔ PROD, message help on hover."),
    ("0.9.0", "2026-10-11", "Journal Explorer, Check Authority, data queues and data areas."),
    ("0.10.0", "2026-10-11", "User interface translated into French, Spanish, German, Italian and Portuguese."),
    ("0.11.0", "2026-10-11", "Work management, users & security, save and restore."),
    ("1.0.0", "2026-10-11", "Storage & cleanup advisor, live alerts, message files."),
    ("1.1.0", "2026-10-11", "Export/import Excel, CSV and JSON; live performance monitor."),
    ("1.2.0", "2026-10-12", "Production and Read-only protection, Self-Check, errors that explain themselves."),
    ("1.3.0", "2026-10-12", "DSPF screen preview, database diagram, compare two systems."),
    ("2.0.0", "2026-10-12", "20 new features: RPG code generation for tables, SQL formatter, find & replace across members."),
    ("2.1.0", "2026-10-12", "Security Admin centre for *SECADM users."),
    ("2.2.0", "2026-10-15", "System Tracker: the whole system on one page."),
    ("2.3.0", "2026-10-17", "Create libraries and IFS files from anywhere; automatic reconnect."),
    ("2.4.0", "2026-10-26", "Local development: deploy changes to the IFS, compile local files, build projects."),
    ("2.5.0", "2026-11-03", "AI with data protection: secrets, personal data and sensitive columns masked."),
    ("2.6.0", "2026-11-03", "About 150 everyday RPG features and 19 new code checks."),
    ("3.0.0", "2026-11-04", "GO menus AS/400-style, import from Code for IBM i, team setup files, code health report."),
    ("3.1.0", "2026-11-04", "DDS checks, CL formatter, RPG semantic highlighting."),
    ("3.2.0", "2026-11-05", "Visual insights: Library Space Map, Batch Job Timeline, Index Advice Chart."),
    ("3.2.1", "2026-11-05", "Fix: IFS Space Map on home folders."),
    ("3.3.0", "upcoming", "Security Audit Journal heat map, Disk Units Map, embedded SQL statistics."),
  ],
 },
 {
  "slug": "salesforce-devpilot-pack", "skills": "Salesforce DX, Apex, LWC, Aura, Flows, metadata dependency graphs, risk scoring, VS Code API, GitLab & Jenkins reporting", "name": "Salesforce DevPilot Pack", "date": "2026-10-18",
  "tagline": "A Salesforce developer pack for VS Code built around a Change Impact Analyzer, with health and release checks that run locally.",
  "tags": ["VS Code", "Salesforce", "Apex / LWC", "CI reports"],
  "repo": f"{GH}/Salesforce-DevPilot-Pack", "release_key": "Salesforce-DevPilot-Pack",
  "latest": "1.0.0", "download": f"{GH}/Salesforce-DevPilot-Pack/releases/latest", "download_label": "Release v1.0.0",
  "image": "devpilot-icon.png", "image_kind": "icon",
  "blog_title": "Salesforce DevPilot Pack: know what your change will break",
  "dek": "Bringing my Salesforce years back into VS Code with dependency graphs, risk scores and one-click release checks.",
  "read": 5,
  "body": """
<p>Before IBM i and Java, I spent years building on Salesforce, and the question that always came up before a release was "what else does this change touch?". Salesforce DevPilot Pack, released on 18 October 2026, answers it inside VS Code, and all the analysis runs locally.</p>
<h2>What's in the pack</h2>
<ul>
<li><strong>Change Impact Analyzer.</strong> Builds a dependency graph of the SFDX project (Apex, triggers, LWC, Aura, Flows, Visualforce, objects, fields, permission sets) and follows every dependent of your changes, with the dependency path, for example <code>Region__c → AccountService → accountList</code>.</li>
<li><strong>Risk score from 0 to 100</strong>, weighted by component type, depth, deletions and findings such as SOQL/DML in loops, tests without assertions, <code>SeeAllData=true</code> and changed Apex with no test.</li>
<li><strong>Recommended tests</strong> that cover the changed code, runnable in one click.</li>
<li><strong>One-click Health Check and Release Check</strong>, an Apex Log Analyzer and Test Intelligence.</li>
<li><strong>GitLab and Jenkins reports</strong> through a small CLI with no npm dependencies.</li>
</ul>
<p>It also installs the standard Salesforce Extension Pack, Prettier, the XML extension and ESLint, so one install sets up a full workstation.</p>
""",
  "history": [("0.1.0", "2026-10-18", "First build."), ("1.0.0", "2026-10-18", "First public release on GitHub.")],
 },
 {
  "slug": "devflow", "skills": "VS Code API, TypeScript, Git hooks & secret scanning, Maven/Gradle/npm/Python build diagnostics, REST tooling", "name": "DevFlow", "date": "2026-10-19",
  "tagline": "One VS Code extension for the daily developer workflow: Environment Doctor, Git Assistant, Build Doctor, API Workspace and a Project Dashboard.",
  "tags": ["VS Code", "TypeScript", "Developer productivity"],
  "repo": None, "release_key": None,
  "latest": "0.1.0", "download": None, "download_label": "Available on request",
  "image": "devflow-icon.png", "image_kind": "icon",
  "blog_title": "DevFlow: a productivity toolkit that works offline",
  "dek": "Checking environments, guarding commits and diagnosing failed builds, with no AI subscription required.",
  "read": 5,
  "body": """
<p>Many lost hours are not spent on hard problems. They go to a missing <code>node_modules</code>, a JDK that is one version too old, a secret pushed by accident, or a Jenkins log nobody wants to read. DevFlow, first built on 19 October 2026, deals with those small problems in one place, and it works offline.</p>
<h2>Five tools in one</h2>
<ul>
<li><strong>Environment Doctor.</strong> Detects the project's stacks (Node, Java Maven/Gradle, Python, Go, .NET, Rust, Docker, Make), checks the required tools and versions, compares <code>.env</code> with <code>.env.example</code>, and offers one-click fixes.</li>
<li><strong>Git Assistant.</strong> Summarises changes, scans added lines for secrets with 15 rules, writes a Conventional Commit message, and runs pre-commit and pre-push checks.</li>
<li><strong>Build Doctor.</strong> More than 45 rules for Maven, Gradle, javac, SSL certificates, npm, Node, TypeScript, Jest and Python, applied to a selection, a log file, the clipboard or a build it runs for you.</li>
<li><strong>API Workspace.</strong> <code>.http</code> and <code>.rest</code> files with Send Request and Compare Environments.</li>
<li><strong>Project Dashboard.</strong> The state of the project on a single page.</li>
</ul>
<p>DevFlow 0.1.0 is packaged as a <code>.vsix</code>. It is not on GitHub yet; contact me if you would like to try it.</p>
""",
  "history": [("0.1.0", "2026-10-19", "First release: Environment Doctor, Git Assistant, Build Doctor, API Workspace, Project Dashboard.")],
 },
 {
  "slug": "jarpilot", "skills": "IBM i IFS & PASE (QSH), CL (CRTBNDCL, CHGAUT, CHGOWN), SSH, PowerShell, Bash, SHA-256 integrity, atomic deployment & rollback, VS Code extension", "name": "JarPilot for IBM i", "date": "2026-10-10",
  "tagline": "Fast, safe JAR installation on the IBM i IFS: validate, checksum, back up, replace atomically and roll back with one command.",
  "tags": ["IBM i", "Shell / PASE", "PowerShell", "CL"],
  "repo": f"{GH}/jatpilot", "release_key": "jatpilot",
  "latest": "1.2.1", "download": f"{GH}/jatpilot/releases", "download_label": "Releases",
  "image": None,
  "blog_title": "JarPilot: deploying JARs to IBM i without the drama",
  "dek": "Every install validated, checksummed, backed up and logged, with rollback one command away.",
  "read": 4,
  "body": """
<p>Copying a JAR into the IFS sounds simple until a half-written file, a wrong owner or a missing backup takes a server down. JarPilot, started on 10 October 2026, turns that copy into a repeatable, safe procedure.</p>
<h2>How each install works</h2>
<p>Validate the JAR → SHA-256 check → back up the current JAR → atomic replace → <code>CHGAUT</code>/<code>CHGOWN</code> → optional restart CL → log and history. If something is wrong, a single <code>rollback</code> restores the previous version, and <code>-DryRun</code> previews every step first.</p>
<h2>Use it from anywhere</h2>
<ul>
<li><strong>From Windows:</strong> <code>jarpilot.ps1</code> uploads and installs over SSH in one command.</li>
<li><strong>On IBM i:</strong> <code>jarpilot.sh</code> runs in PASE/QSH.</li>
<li><strong>From 5250 or the job scheduler:</strong> a CL wrapper, <code>CALL JARPILOT</code>.</li>
<li><strong>From the editor:</strong> a VS Code extension. Right-click a <code>.jar</code> and choose <em>Install</em>.</li>
<li><strong>Server setup:</strong> upload a setup JAR and JarPilot answers the installer's questions, checking each answer on the IBM i first so a second server never reuses an existing directory or library.</li>
</ul>
""",
  "history": [("1.0.0", "2026-10-10", "First release: core installer, PowerShell and CL wrappers."),
              ("1.1.0", "2026-10-13", "Guided server setup from a setup JAR."),
              ("1.2.1", "2026-10-13", "VS Code extension (.vsix) and assistant plugin.")],
 },
 {
  "slug": "routinel", "skills": "Static analysis of Express/NestJS/Spring/FastAPI/Django routes, OpenAPI 3, Postman v2.1, VS Code SecretStorage, mock servers, TypeScript", "name": "Routinel – API Finder & Client", "date": "2026-10-09",
  "tagline": "Finds every HTTP API in your workspace, in any supported language, and calls it from a built-in Postman-style client.",
  "tags": ["VS Code", "TypeScript", "REST", "OpenAPI"],
  "repo": f"{GH}/dataman-api-lens", "release_key": "dataman-api-lens",
  "latest": "1.3.0", "download": f"{GH}/dataman-api-lens/releases/latest", "download_label": "VS Code extension (.vsix)",
  "image": "routinel-client.png", "image_kind": "figure",
  "blog_title": "Routinel: find every API in your code and call it",
  "dek": "Route + Sentinel: endpoint discovery, a Postman-style client and a mock server, all inside VS Code.",
  "read": 5,
  "body": """
<p>Joining a new code base usually starts with the same question: which endpoints does this service expose, and what do they expect? Routinel (from <em>Route</em> and <em>Sentinel</em>), first released on 9 October 2026, scans the workspace and answers it, then lets you call each endpoint without leaving the editor.</p>
<figure><img src="../media/projects/routinel-client.png" alt="Routinel request and response view"><figcaption>The built-in client: params, headers, body, auth and a pretty-printed response.</figcaption></figure>
<h2>Highlights</h2>
<ul>
<li><strong>Automatic discovery</strong> across Express, Koa, Fastify, NestJS, Next.js, FastAPI, Flask, Django/DRF, Spring and more, including router prefixes and context paths.</li>
<li><strong>Parameters from code:</strong> path, query, headers, cookies, form fields, uploads and JSON bodies generated from your DTOs and models.</li>
<li><strong>A Postman-style client</strong> with environments, secrets kept in the OS keychain, request chaining, collections and history.</li>
<li><strong>Import and export</strong> Postman v2.1 collections and OpenAPI 3, plus code generation for cURL, PowerShell, fetch and Python.</li>
<li><strong>Mock server (1.3.0)</strong> that serves every discovered API locally from saved mocks, OpenAPI examples or generated responses.</li>
</ul>
""",
  "history": [("1.0.0", "2026-10-09", "First release (as Dataman API Lens)."),
              ("1.1.0", "2026-10-09", "Renamed <strong>Routinel</strong>."),
              ("1.1.1", "2026-10-09", "Project names when adding folders or Git repositories."),
              ("1.1.2", "2026-10-09", "Marketplace publisher <code>gauravgupta0612</code>; repository links."),
              ("1.2.1", "2026-10-09", "Maintenance release."),
              ("1.3.0", "2026-10-10", "Mock server for every discovered API.")],
 },
 {
  "slug": "devsuite", "skills": "Monorepo design, shared analysis engine, parsers for JS/TS, Python, Java, Go, C# and IBM i RPG/CL/DDS/SQL/COBOL, dependency graphs, GitHub Actions release pipelines", "name": "DevSuite", "date": "2026-10-09",
  "tagline": "One shared analysis engine and five focused VS Code extensions: RepoPilot, DevImpact, CodeGuard, TraceLens and BugTrail.",
  "tags": ["VS Code", "Monorepo", "Static analysis", "IBM i"],
  "repo": f"{GH}/devsuite", "release_key": "devsuite",
  "latest": "0.1", "download": f"{GH}/devsuite/releases", "download_label": "VS Code extensions (.vsix)",
  "image": None,
  "blog_title": "DevSuite: one engine, five focused extensions",
  "dek": "Why I split one large idea into small tools that share a single code-analysis core.",
  "read": 5,
  "body": """
<p>Large extensions that try to do everything end up doing nothing well. DevSuite, started on 9 October 2026, takes the opposite approach: one shared analysis engine (<code>@devsuite/core</code>, with no VS Code dependency) and several small extensions, each focused on one job and each released on its own.</p>
<h2>The five extensions</h2>
<ul>
<li><strong>RepoPilot:</strong> architecture, entry points, build commands, modules, a dependency map and an onboarding guide.</li>
<li><strong>DevImpact:</strong> what a change affects, an impact score, and which tests to run.</li>
<li><strong>CodeGuard:</strong> a prioritised risk report for changes (secrets, security, regressions, tests, config and IBM i), also available as a CLI and a pre-commit hook.</li>
<li><strong>TraceLens:</strong> every API endpoint, traced through to database and external calls.</li>
<li><strong>BugTrail:</strong> a searchable history of errors, attempts and fixes that warns you when a fixed bug comes back.</li>
</ul>
<p>The engine indexes JavaScript/TypeScript, Python, Java/Kotlin, Go, C# and IBM i RPG, CL, DDS, SQL and COBOL. The <strong>DevSuite Pack</strong> installs all five at once. Each extension has its own GitHub Actions release workflow.</p>
""",
  "history": None,
 },
 {
  "slug": "ibm-i-zos-explorer", "skills": "IBM i (SSH, SQL, CL, spool, QSYSOPR), z/OS (z/OSMF REST, JCL, TSO, MVS console, PDS/PDSE, USS), VS Code API, TypeScript", "name": "IBM i & z/OS Explorer", "date": "2026-10-09",
  "tagline": "One VS Code sidebar for IBM i (SSH + SQL) and z/OS (z/OSMF): data sets, members, IFS, USS, JCL, spool and commands.",
  "tags": ["VS Code", "IBM i", "z/OS", "z/OSMF"],
  "repo": f"{GH}/IBM-i-z-OS-Explorer", "release_key": "IBM-i-z-OS-Explorer",
  "docs": "https://gauravgupta0612.github.io/IBM-i-z-OS-Explorer-doc/",
  "latest": "1.1.0", "download": f"{GH}/IBM-i-z-OS-Explorer/releases/latest", "download_label": "VS Code extension (.vsix)",
  "image": None,
  "blog_title": "IBM i & z/OS Explorer: two platforms, one sidebar",
  "dek": "A single extension for developers who work on both IBM midrange and mainframe systems.",
  "read": 4,
  "body": """
<p>Many enterprise developers move between IBM i and z/OS during the same week, and usually need two sets of tools to do it. IBM i &amp; z/OS Explorer, released on 9 October 2026, puts both behind one icon in the VS Code sidebar.</p>
<h2>z/OS, over z/OSMF REST</h2>
<ul>
<li>Data sets, PDS/PDSE members and USS files: browse, edit and save back, with an ETag check if someone else changed the member.</li>
<li>Submit JCL, follow jobs and read spool output; run TSO and MVS console commands.</li>
<li>Search inside a PDS, copy and rename members, view data set attributes, and generate compile/link/run JCL from templates (1.1.0).</li>
</ul>
<h2>IBM i, over SSH and SQL</h2>
<ul>
<li>Libraries, source members and IFS; library list and current library; compile with errors in <em>Problems</em>.</li>
<li>Run CL and SQL (sortable grid with CSV export), view spooled files, active jobs and job logs, and reply to QSYSOPR messages.</li>
<li>Object actions such as DSPOBJD, DSPPGMREF and DSPFFD, plus an SSH (PASE) terminal.</li>
</ul>
<p>Documentation: <a href="https://gauravgupta0612.github.io/IBM-i-z-OS-Explorer-doc/">IBM i &amp; z/OS Explorer docs</a>.</p>
""",
  "history": [("1.0.0", "2026-10-09", "First release: z/OS via z/OSMF, IBM i via SSH + SQL."),
              ("1.1.0", "2026-10-09", "Search in PDS, copy/rename members and data sets, data set attributes.")],
 },
]

# Order used on the downloads page and project list (newest first by start date)
ORDER = ["ai-native-dev-platform", "tavrion-studio", "devflow", "salesforce-devpilot-pack", "jarpilot",
         "routinel", "devsuite", "ibm-i-zos-explorer", "vanthrex-for-ibm-i"]
