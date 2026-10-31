# petertessier-blog

Peter Tessier's Jekyll-based blog.

## Hosting locally

Requires Ruby + Bundler installed.

```powershell
bundle install
bundle exec jekyll serve --livereload
```

Then open `http://localhost:4000`.

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
