# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A self-paced **staff AI training website** for a school (Marriotts, a Microsoft A3 school).
**Static HTML only** — no framework, no build step, no dependencies, no package.json. Every page
is a self-contained `.html` file with all CSS and JS inline. There is nothing to compile.

- `index.html` — the hub / dashboard (pathway picker, progress, links to every module)
- `*-module.html` — the 13 training modules
- `staff-launch-message.md`, `it-brief-*.md` — supporting docs, not part of the website

## Architecture

**Three pathways, 13 modules**, each a standalone interactive lesson following the same 8-section
structure (hook → idea → worked example → hands-on task → data-safety checkpoint → self-check →
where-next). Pathways are colour-coded by header gradient — a **Marriotts-branded triad**:
**Foundations = coral-red `#d0452e`**, **Practitioner = slate-teal `#3f6e72`**, **Builder = charcoal
`#565b5e`** (each also has a `-deep` and `-tint` shade). Module order:
F1 what-is-ai → F2 safe-uses → F3 which-tool → F4 prompting → P1 model-thinking → P2 power-modes →
P3 images → P4 video → P5 custom-assistant → B1 chat-to-app → B2 vibe-coding → B3 agentic-landscape →
B4 share-responsibly.

**Branding.** Brand colours are coral `#d0452e` + grey `#73797c`, taken from the school's official
`logo.svg` (repo root). The logo sits in every page header (white rounded tile + the eyebrow
"Marriotts School · Staff AI Programme") and is the favicon (`<link rel="icon" href="logo.svg">`).
New pages must include both. **Don't recolour the in-lesson illustrative legends** (F4's
role/context/constraints/format prompt-part colours, the image SSCC legend, etc.) — those are
separate CSS vars used for teaching, not pathway theming.

**Progress tracking.** Modules are otherwise storage-free (in-memory JS only, no external calls), with
**one exception**: each module's "Where next" section has save links that record completion. The
dashboard reads it back.
- Storage keys: `localStorage['saip_done']` = JSON array of completed module ids (e.g. `["F1","P2"]`);
  `localStorage['saip_tool']` = the user's preferred tool string.
- `index.html` renders pathways/progress from `saip_done` and re-reads it on `pageshow`, `focus`,
  `visibilitychange` and `storage` events (so an already-open dashboard never shows stale numbers).
  It shows a red banner if `localStorage` is blocked (private window), and has a **progress-code**
  panel (base64 export/import of `{d,t}`) so users can carry progress between devices.

**The module generator.** Modules are produced by the `anthropic-skills:staff-ai-training-module`
skill (blueprint + per-tool notes). The shared design system and module conventions are documented in
the user's memory files (`staff-ai-training-system.md`, `ai-training-module-design-system.md`). New
modules must match the design system and include the save links described below.

## CRITICAL: Netlify corrupts inline `onclick` on `<a>` tags

Netlify's **"Pretty URLs"** asset optimisation rewrites every `<a href>` (`.html` → clean URL) and,
when re-serialising the anchor, **invalidly escapes single quotes inside an inline `onclick`** (turns
`getItem('saip_done')` into `getItem(\'saip_done\')`), silently breaking the handler **on the live
site only** — local files and the GitHub source stay correct, which makes this very hard to diagnose.
`netlify.toml`'s `skip_processing` did **not** override it (the optimisation is forced on in the
Netlify UI).

**Therefore: never put an inline `onclick` (or any quote-containing inline JS) on an `<a href>` tag.**
The save links use a `data-done="<ID>"` attribute plus a script-block listener that does the write:

```js
document.querySelectorAll('a[data-done]').forEach(function(a){
  a.addEventListener('click', function(){
    try{ var id=a.getAttribute('data-done');
         var d=JSON.parse(localStorage.getItem('saip_done')||'[]');
         if(d.indexOf(id)<0){ d.push(id); localStorage.setItem('saip_done',JSON.stringify(d)); } }
    catch(e){}
  });
});
```

Script-block JS is safe from Pretty URLs. Inline `onclick` on a `<button>` is also safe (Pretty URLs
only touches `<a href>` tags) — only anchors are affected.

## Local development

No build/lint/test. To preview locally, serve the folder over HTTP (relative links + `localStorage`
need a real origin, not `file://`):

```bash
python -m http.server 8765      # then open http://localhost:8765/
```

A `.claude/launch.json` defines a `static` preview server (port 8765) for the preview tooling.

## Deployment

Continuously deployed from GitHub via Netlify. **Editing files → `git commit` → `git push` to `main`
→ Netlify auto-builds & publishes (~1 min).** No Netlify CLI or dashboard step needed.

| Thing | Value |
|---|---|
| GitHub repo | https://github.com/callumpackard82-rgb/marriotts-ai-training |
| Deploy branch | `main` |
| Live URL | https://marriotts-ai-training.netlify.app |
| Build command | *(none — static site)* |
| Publish directory | repository root |

The local folder **is** a git clone connected to `origin` (Git Credential Manager handles auth on
push). `netlify.toml` sets `Cache-Control: must-revalidate` on all pages (so updates aren't masked by
stale cache) and attempts to disable asset post-processing.

After any change affecting the live site, verify by fetching the deployed file (not just trusting the
push) — e.g. `Invoke-WebRequest` the page and check the served HTML, since Netlify can transform it.

## Things to avoid

- **No inline `onclick` on `<a>` tags** (see the CRITICAL section) — this silently breaks saving in prod.
- Don't add a build step, bundler, or `package.json` — it's intentionally plain static HTML.
- Don't change the Netlify publish directory away from repo root, or `index.html` won't be found.
- Don't commit pupil/staff personal data — the only stored data is module-completion flags in the
  browser. Keep example data in modules synthetic/anonymised (the data-safety spine runs through every
  module: real school data only in Microsoft 365 Copilot Chat with the green shield).
- Keep links between pages **relative**. Netlify also serves clean URLs (`/foundations-prompting-module`
  resolves to the `.html`).

## Content conventions

- This is a **secondary school** — keep all examples secondary-appropriate (KS3/KS4 year groups and
  topics, "students" not "children"). Don't use primary-age examples.
- Copilot here = **Microsoft 365 Copilot Chat** only (free with A3, enterprise data protection,
  accessed via Teams/Edge/browser). The school does **not** have the paid in-app Copilot in
  Word/Excel/PowerPoint — never describe it as "built into" the Office apps. (The generator skill's
  tool-notes wrongly assume in-app embedding; ignore that for this deployment.)
