# Project: Staff AI Training Programme

A self-paced staff AI training website. **Static HTML only** — no framework, no build
step, no dependencies. Each page is a self-contained `.html` file.

- `index.html` — the hub / landing page (links to every module)
- `*-module.html` — the individual training modules (foundations / practitioner / builder)
- `staff-launch-message.md` — a launch announcement (not part of the website)

All HTML files live at the **repository root** and link to each other with relative paths.
There is nothing to compile.

---

## Deployment architecture (read before changing how the site is published)

The live site is **continuously deployed from GitHub via Netlify**. The pipeline is:

```
edit files  ->  git commit  ->  git push to `main`  ->  Netlify auto-builds & publishes
```

| Thing | Value |
|---|---|
| GitHub repo | https://github.com/callumpackard82-rgb/marriotts-ai-training |
| Deploy branch | `main` |
| Live URL | https://marriotts-ai-training.netlify.app |
| Netlify build command | *(none — static site)* |
| Netlify publish directory | repository root |

Netlify is linked to the GitHub repo (Netlify project: `marriotts-ai-training`, team
"Head of AI"). **Any push to `main` triggers a deploy automatically**, live in ~1 minute.
You do not need to run any Netlify CLI command or touch the Netlify dashboard to publish —
pushing to GitHub is the whole job.

### Important: the local folder is NOT yet connected to the GitHub repo

This folder currently has the HTML files but is **not a git clone**. The files were placed
on GitHub through the web uploader, not pushed from here, so there is no `.git` and no remote.
The GitHub repo also contains a `README.md` that does not exist locally.

**Before you can push updates, connect this folder to the remote.** One-time setup, run in
this folder:

```bash
git init
git remote add origin https://github.com/callumpackard82-rgb/marriotts-ai-training.git
git fetch origin
git reset origin/main          # aligns history with the remote, keeps your local files
git branch -M main
git branch --set-upstream-to=origin/main main
```

After this, `git status` will show whether your local files differ from what is on GitHub.
Commit and push any real changes:

```bash
git add -A
git commit -m "Describe the change"
git push
```

The first push will require the user's GitHub authentication (Git Credential Manager will
prompt, or use an authenticated `gh` CLI). Do not hard-code or store any token in the repo.

---

## How to update the website

1. Edit the relevant `.html` file(s) directly.
2. Keep links between pages **relative** (e.g. `practitioner-images-module.html`), and note
   Netlify serves clean URLs too — `/practitioner-images-module` resolves to the `.html` file.
3. Commit and push to `main` (see above). Netlify redeploys automatically.
4. Verify at https://marriotts-ai-training.netlify.app after ~1 minute.

## Things to avoid

- Don't add a build step, bundler, or `package.json` unless the site genuinely needs one —
  it is intentionally plain static HTML and the Netlify project has no build command.
- Don't change the Netlify publish directory away from the repo root, or `index.html`
  won't be found.
- Don't commit secrets, tokens, or the user's progress data — the site stores user
  progress in the browser (localStorage), nothing server-side.
