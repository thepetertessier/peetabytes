# Peetabytes

Peter Tessier's Jekyll-based blog.

## Previewing locally

Requires Ruby and Bundler. On Windows, WSL2 with Ubuntu is the recommended setup.

```sh
bundle install
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000`.

## Publishing a new post

1. Add a file to `_posts/` named `YYYY-MM-DD-your-title.md`.
2. Include front matter at the top:
   ```yaml
   ---
   title: "Your Title Here"
   date: YYYY-MM-DD
   categories: [ai, coding]
   tags: [lowercase-tag]
   ---
   ```
   Use no more than two lowercase categories. Chirpy applies the post layout by default.
3. Write in Markdown below the `---`.
4. Push to `main` to deploy through GitHub Actions.
