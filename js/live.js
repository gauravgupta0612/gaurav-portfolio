// Live layer: pulls releases, stars and installs at page load, and adds search, charts and motion.
(function () {
  "use strict";
  const ROOT = window.GG_ROOT || "";
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const DAY = 864e5;
  const fmt = d => new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
  const vkey = t => t.split("-v").pop().replace(/^v/, "");

  const cache = {
    get(k, maxAge) { try { const o = JSON.parse(sessionStorage.getItem(k)); if (o && Date.now() - o.t < maxAge) return o.v; } catch (e) {} return null; },
    set(k, v) { try { sessionStorage.setItem(k, JSON.stringify({ t: Date.now(), v })); } catch (e) {} }
  };
  const getJSON = async (url, opts) => { const r = await fetch(url, opts); if (!r.ok) throw new Error(r.status); return r.json(); };

  const state = { site: null, releases: {}, market: { extensions: [] }, stars: {}, live: false };

  // ---------- data ----------
  async function loadStatic() {
    const [site, rel, mkt] = await Promise.allSettled([
      getJSON(ROOT + "data/site.json"), getJSON(ROOT + "data/releases.json"), getJSON(ROOT + "data/marketplace.json", { cache: "no-cache" })]);
    if (site.status === "fulfilled") state.site = site.value;
    if (rel.status === "fulfilled") state.releases = rel.value;
    if (mkt.status === "fulfilled") state.market = mkt.value;
  }

  async function loadLive() {
    if (!state.site) return;
    const owner = state.site.owner, key = "gg-live-v1";
    const hit = cache.get(key, 15 * 60 * 1000);
    if (hit) { Object.assign(state.releases, hit.releases); state.stars = hit.stars; state.live = hit.when; return; }
    const repos = [...new Set(state.site.projects.map(p => p.release_key).filter(Boolean))];
    const out = { releases: {}, stars: {} };
    await Promise.all(repos.map(async r => {
      try {
        const [rels, info] = await Promise.all([
          getJSON(`https://api.github.com/repos/${owner}/${r}/releases?per_page=50`),
          getJSON(`https://api.github.com/repos/${owner}/${r}`)]);
        out.releases[r] = rels.filter(x => !x.draft).map(x => {
          const old = (state.releases[r] || []).find(o => o.tag === x.tag_name);
          return { tag: x.tag_name, date: x.published_at.slice(0, 10), name: x.name || x.tag_name, url: x.html_url,
                   summary: old ? old.summary : summarize(x.body),
                   assets: x.assets.map(a => ({ name: a.name, url: a.browser_download_url, size: a.size })) };
        });
        out.stars[r] = info.stargazers_count;
      } catch (e) { /* rate limit or offline: keep saved data */ }
    }));
    if (Object.keys(out.releases).length) {
      out.when = Date.now();
      Object.assign(state.releases, out.releases); state.stars = out.stars; state.live = out.when;
      cache.set(key, out);
    }
  }

  function summarize(body) {
    for (const line of String(body || "").split("\n")) {
      const t = line.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/[*_`#>]/g, "").replace(/^[\s\-:]+|[\s\-:]+$/g, "");
      if (t.length > 12 && !/^(full changelog|download|what's changed)/i.test(t)) return t.length > 220 ? t.slice(0, 220) + "…" : t;
    }
    return "";
  }

  // ---------- render ----------
  function allReleases() {
    const list = [];
    (state.site ? state.site.projects : []).forEach(p => (state.releases[p.release_key] || []).forEach(r => list.push({ p, r })));
    return list.sort((a, b) => b.r.date.localeCompare(a.r.date));
  }
  const isNew = d => Date.now() - new Date(d + "T00:00:00") < 7 * DAY;

  function renderFeed(list) {
    const ul = $("#updatesList"); if (!ul || !list.length) return;
    ul.innerHTML = list.slice(0, 8).map(({ p, r }) => {
      const dl = r.assets && r.assets[0] ? r.assets[0].url : r.url;
      return `<li class="in"><time datetime="${r.date}">${fmt(r.date)}</time>
        <div class="upd-body"><div class="upd-title"><a href="${ROOT}blog/${p.slug}.html">${esc(r.name)}</a><span class="ver">${esc(r.tag)}</span>${isNew(r.date) ? '<span class="new">NEW</span>' : ""}</div>
        ${r.summary ? `<p>${esc(r.summary)}</p>` : ""}</div>
        <div class="upd-act"><a class="btn primary sm" href="${dl}"><i class="fas fa-download"></i> ${r.assets && r.assets.length ? "Download" : "Release"}</a></div></li>`;
    }).join("");
  }

  function installsFor(p) {
    const xs = state.market.extensions.filter(e => p.ext.includes(e.id.split(".").slice(1).join(".")));
    return { n: xs.reduce((a, e) => a + e.installs, 0), xs };
  }

  function renderCards() {
    if (!state.site) return;
    state.site.projects.forEach(p => {
      const card = $(`.project[data-slug="${p.slug}"]`); if (!card) return;
      const rels = state.releases[p.release_key] || [];
      if (rels.length && p.slug !== "devsuite") { const v = $('[data-live="ver"]', card); if (v) v.textContent = "v" + vkey(rels[0].tag); }
      if (rels.length && isNew(rels[0].date) && !$(".ribbon", card)) card.insertAdjacentHTML("afterbegin", '<span class="ribbon">New release</span>');
      const st = state.stars[p.release_key];
      const sEl = $('[data-live="stars"]', card);
      if (sEl && st) { sEl.hidden = false; sEl.innerHTML = `<i class="fab fa-github"></i> ${st} ★`; }
      const inst = installsFor(p), iEl = $(".installs", card);
      if (iEl && inst.n) { const one = inst.xs.length === 1 && inst.xs[0].rating ? ` · <i class="fas fa-star"></i> ${inst.xs[0].rating.toFixed(1)}` : ""; iEl.innerHTML = `<i class="fas fa-download"></i> ${inst.n.toLocaleString()} installs${one}`; }
    });
  }

  function setCount(el, n) { if (!el) return; el.dataset.count = n; el.textContent = n.toLocaleString(); }
  function renderStats(list) {
    setCount($("#statReleases"), list.length);
    const total = state.market.extensions.reduce((a, e) => a + e.installs, 0);
    if (total) setCount($("#statInstalls"), total);
    const v = $("#vanthrexLive"), vr = state.releases["silverlake-ibmi"] || [];
    const vi = state.market.extensions.find(e => e.id.endsWith(".vanthrex-ibmi"));
    if (v && vr.length) v.textContent = `v${vkey(vr[0].tag)} · ${vi ? vi.installs.toLocaleString() + " installs · " : ""}${vr.length} releases`;
    const pill = $("#livePill"), txt = $("#liveText");
    if (pill && state.live) { pill.classList.add("on"); txt.textContent = "Live from GitHub · checked " + new Date(state.live).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }); }
  }

  function renderActivity(list) {
    const box = $("#activity"); if (!box || !list.length) return;
    const weeks = 12, now = new Date(), start = new Date(now - (weeks * 7 - 1) * DAY);
    const bins = Array.from({ length: weeks }, (_, i) => ({ from: new Date(+start + i * 7 * DAY), n: 0, names: [] }));
    list.forEach(({ p, r }) => { const d = new Date(r.date + "T12:00:00"); const i = Math.floor((d - start) / (7 * DAY)); if (i >= 0 && i < weeks) { bins[i].n++; bins[i].names.push(p.name.split(" – ")[0] + " " + r.tag); } });
    const max = Math.max(1, ...bins.map(b => b.n)), total = bins.reduce((a, b) => a + b.n, 0);
    box.innerHTML = bins.map(b => `<div class="bar" title="${esc(b.from.toLocaleDateString("en-GB", { day: "numeric", month: "short" }))}: ${b.n} release${b.n === 1 ? "" : "s"}${b.names.length ? "\n" + esc(b.names.slice(0, 6).join(", ")) : ""}">
      <span style="--h:${(b.n / max) * 100}%"><em>${b.n || ""}</em></span><small>${b.from.toLocaleDateString("en-GB", { day: "numeric", month: "short" })}</small></div>`).join("");
    const s = $("#activitySum"); if (s) s.textContent = `${total} releases in the last ${weeks} weeks`;
  }

  function toastNewest(list) {
    if (!list.length || !isNew(list[0].r.date)) return;
    const k = "gg-toast-" + list[0].r.tag + list[0].p.slug; if (cache.get(k, 864e5)) return; cache.set(k, 1);
    const t = document.createElement("a");
    t.className = "toast"; t.href = ROOT + "blog/" + list[0].p.slug + ".html";
    t.innerHTML = `<i class="fas fa-bolt"></i><div><strong>New release</strong><span>${esc(list[0].r.name)}</span></div>`;
    document.body.appendChild(t); requestAnimationFrame(() => t.classList.add("show"));
    setTimeout(() => t.classList.remove("show"), 6500);
  }

  // ---------- command palette ----------
  function palette() {
    const box = $("#palette"), input = $("#paletteInput"), ul = $("#paletteList"); if (!box) return;
    let items = [], sel = 0;
    const build = () => {
      const s = state.site || { projects: [], posts: [], pages: [] };
      items = [
        ...s.projects.map(p => ({ icon: "fa-cube", group: "Project", title: p.name, sub: p.tagline, url: ROOT + "blog/" + p.slug + ".html", kw: p.tags.join(" ") })),
        ...s.posts.map(p => ({ icon: "fa-feather", group: "Journal", title: p.title, sub: p.dek, url: ROOT + "blog/" + p.slug + ".html" })),
        ...allReleases().slice(0, 40).map(({ p, r }) => ({ icon: "fa-tag", group: "Release", title: r.name, sub: fmt(r.date) + (r.summary ? " · " + r.summary : ""), url: r.assets && r.assets[0] ? r.assets[0].url : r.url, kw: r.tag })),
        ...state.market.extensions.map(e => ({ icon: "fa-store", group: "Marketplace", title: e.name, sub: e.installs.toLocaleString() + " installs · v" + e.version, url: "https://marketplace.visualstudio.com/items?itemName=" + e.id })),
        ...s.pages.map(([t, u]) => ({ icon: "fa-file", group: "Page", title: t, sub: "", url: ROOT + u })),
        { icon: "fa-circle-half-stroke", group: "Action", title: "Switch light / dark theme", sub: "", act: () => $(".theme-btn") && $(".theme-btn").click() },
        { icon: "fab fa-github", group: "Link", title: "GitHub profile", sub: "github.com/gauravgupta0612", url: "https://github.com/gauravgupta0612" }
      ];
    };
    const render = () => {
      const q = input.value.trim().toLowerCase();
      const words = q.split(/\s+/).filter(Boolean);
      const hits = items.filter(i => words.every(w => (i.title + " " + i.sub + " " + (i.kw || "") + " " + i.group).toLowerCase().includes(w))).slice(0, 12);
      sel = Math.min(sel, Math.max(0, hits.length - 1));
      ul.innerHTML = hits.length ? hits.map((i, n) => `<li role="option" class="${n === sel ? "sel" : ""}" data-n="${n}"><i class="${i.icon.startsWith("fab") ? i.icon : "fas " + i.icon}"></i><div><strong>${esc(i.title)}</strong>${i.sub ? `<span>${esc(i.sub)}</span>` : ""}</div><em>${i.group}</em></li>`).join("") : '<li class="empty">No results</li>';
      ul._hits = hits;
    };
    const go = n => { const i = (ul._hits || [])[n]; if (!i) return; close(); if (i.act) i.act(); else location.href = i.url; };
    const open = () => { build(); box.hidden = false; input.value = ""; sel = 0; render(); setTimeout(() => input.focus(), 10); document.body.style.overflow = "hidden"; };
    const close = () => { box.hidden = true; document.body.style.overflow = ""; };
    $$("[data-palette]").forEach(b => b.addEventListener("click", open));
    box.addEventListener("click", e => { if (e.target === box) close(); const li = e.target.closest("li[data-n]"); if (li) go(+li.dataset.n); });
    input.addEventListener("input", () => { sel = 0; render(); });
    document.addEventListener("keydown", e => {
      const typing = /input|textarea/i.test((e.target.tagName || "")) && e.target !== input;
      if ((e.key === "k" && (e.ctrlKey || e.metaKey)) || (e.key === "/" && !typing && box.hidden)) { e.preventDefault(); box.hidden ? open() : close(); return; }
      if (box.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowDown") { e.preventDefault(); sel = Math.min(sel + 1, (ul._hits || []).length - 1); render(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); sel = Math.max(sel - 1, 0); render(); }
      else if (e.key === "Enter") { e.preventDefault(); go(sel); }
    });
  }

  // ---------- motion ----------
  function rotator() {
    const el = $(".rotator"); if (!el || reduce) return;
    const words = el.dataset.words.split("|"); let i = 0;
    el.textContent = words[0];
    setInterval(() => { el.classList.add("out"); setTimeout(() => { i = (i + 1) % words.length; el.textContent = words[i].replace(/&amp;/g, "&"); el.classList.remove("out"); }, 350); }, 2600);
  }
  function tilt() {
    if (reduce || matchMedia("(hover: none)").matches) return;
    $$(".tilt, .card").forEach(c => {
      c.addEventListener("mousemove", e => {
        const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.style.setProperty("--mx", x * 100 + "%"); c.style.setProperty("--my", y * 100 + "%");
        if (c.classList.contains("tilt")) c.style.transform = `perspective(900px) rotateX(${(0.5 - y) * 5}deg) rotateY(${(x - 0.5) * 6}deg) translateY(-4px)`;
      });
      c.addEventListener("mouseleave", () => { c.style.transform = ""; });
    });
  }

  // ---------- start ----------
  async function start() {
    palette(); rotator(); tilt();
    await loadStatic();
    let list = allReleases(); renderActivity(list); renderCards(); renderStats(list);
    await loadLive();
    list = allReleases();
    renderFeed(list); renderActivity(list); renderCards(); renderStats(list); toastNewest(list);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
