# petertessier-blog

Jekyll scaffold for blog.petertessier.com, built to run on GitHub Pages
with zero build config.

## One-time setup

1. Create a new **public** repo on GitHub (name doesn't matter, e.g. `blog`).
2. Push this folder to it:
   ```
   git init
   git add .
   git commit -m "Initial blog scaffold"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```
3. In the repo: **Settings → Pages** → set source to the `main` branch,
   root folder. The `CNAME` file already in this repo will populate the
   custom domain field automatically.
4. At your domain registrar, add a DNS record:
   - Type: `CNAME`
   - Host: `blog`
   - Value: `YOUR-USERNAME.github.io`
5. Back in Settings → Pages, once GitHub verifies the domain, check
   **Enforce HTTPS**.
6. Update the placeholders in `_config.yml` (email, LinkedIn/GitHub links).

DNS can take anywhere from a few minutes to a few hours to propagate.

## Writing locally (optional but nice)

Requires Ruby + Bundler installed.

```
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000` — it live-reloads as you edit.

You don't strictly need this — editing markdown on GitHub.com directly
and pushing also works fine, especially for short posts.

## Publishing a new post

1. Add a file to `_posts/` named `YYYY-MM-DD-your-title.md`.
2. Include front matter at the top:
   ```yaml
   ---
   layout: post
   title: "Your Title Here"
   date: YYYY-MM-DD
   categories: [tag1, tag2]
   ---
   ```
3. Write in markdown below the `---`.
4. Commit and push. Live in about a minute.

## Cross-posting to LinkedIn

Manual, by design: write 2-3 sentences on the core takeaway, link to
the full post at `https://blog.petertessier.com/YYYY/MM/DD/your-title/`.
