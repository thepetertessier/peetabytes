Add to this file any lessons learned the hard way to help future runs.

- This repo uses LF line endings. Some edit tools may rewrite files as CRLF; after editing, check `git diff --stat` and normalize if a whole file shows as changed.
- On this Windows machine, Ruby 3.2 has the blog's installed gems; Ruby 3.4 currently does not. If the default runtime fails, use `C:/Ruby32-x64/bin/ruby.exe C:/Ruby32-x64/bin/bundle exec jekyll serve --host 127.0.0.1 --port 4000`.
