#!/usr/bin/env python3
"""Send Jekyll posts to Buttondown as emails.

Usage:
    python scripts/send_to_buttondown.py [--dry-run] _posts/2026-11-01-my-post.md ...

Environment variables:
    BUTTONDOWN_API_KEY      API key (required unless --dry-run)
    BUTTONDOWN_MODE         "draft" (default) creates a draft you send by hand.
                            "send" queues it to your subscribers immediately.
    SITE_URL                Default: https://blog.petertessier.com
    POST_URL_PATTERN        Where a post lives on the site. Placeholders:
                            {year} {month} {day} {slug}
                            Default: /{year}/{month}/{day}/{slug}/
    ADD_READ_ON_WEB_LINK    "true" adds a "Read on the web" link at the top.
                            Default: false

Opt a post out of the newsletter with `newsletter: false` in its front matter.
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

API_URL = "https://api.buttondown.com/v1/emails"
API_VERSION = "2026-04-01"
USER_AGENT = "jekyll-buttondown-action"  # default python UA can get blocked

SITE_URL = os.environ.get("SITE_URL", "https://blog.petertessier.com").rstrip("/")
POST_URL_PATTERN = os.environ.get(
    "POST_URL_PATTERN", "/{year}/{month}/{day}/{slug}/"
)
MODE = os.environ.get("BUTTONDOWN_MODE", "draft").strip().lower()
ADD_WEB_LINK = os.environ.get("ADD_READ_ON_WEB_LINK", "false").strip().lower() == "true"

FILENAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.(?:md|markdown)$")
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.S)
# Anything not already absolute / special: leave those alone.
RELATIVE = r"(?!https?://|mailto:|tel:|#|data:|//)"


def parse_post(path):
    text = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"{path}: no front matter found")
    front = yaml.safe_load(match.group(1)) or {}
    return front, match.group(2).strip()


def post_url(path, front):
    if front.get("permalink"):
        return f"{SITE_URL}/{str(front['permalink']).lstrip('/')}"
    name_match = FILENAME_RE.match(Path(path).name)
    if not name_match:
        raise ValueError(f"{path}: filename should look like YYYY-MM-DD-title.md")
    year, month, day, slug = name_match.groups()
    rel = POST_URL_PATTERN.format(year=year, month=month, day=day, slug=slug)
    return f"{SITE_URL}/{rel.lstrip('/')}"


def absolutize(path):
    return f"{SITE_URL}{path if path.startswith('/') else '/' + path}"


def prepare_body(body):
    """Make the post Markdown work outside the site: absolute links, no Liquid basics."""
    # {{ "/assets/x.png" | relative_url }}  ->  https://site/assets/x.png
    body = re.sub(
        r"""\{\{\s*["']([^"']+)["']\s*\|\s*(?:relative_url|absolute_url)\s*\}\}""",
        lambda m: absolutize(m.group(1)),
        body,
    )
    body = re.sub(r"\{\{\s*site\.url\s*\}\}", SITE_URL, body)
    body = re.sub(r"\{\{\s*site\.baseurl\s*\}\}", "", body)

    # Markdown links/images: [text](/path) and ![alt](path)
    body = re.sub(
        r"(\]\()" + RELATIVE + r"([^)\s]+)",
        lambda m: m.group(1) + absolutize(m.group(2)),
        body,
    )
    # Inline HTML: src="/path" href="/path"
    body = re.sub(
        r"""((?:src|href)\s*=\s*["'])""" + RELATIVE + r"""([^"']+)""",
        lambda m: m.group(1) + absolutize(m.group(2)),
        body,
    )

    if "{%" in body or "{{" in body:
        print(
            "  WARNING: leftover Liquid ({% %} or {{ }}) in post; "
            "check the email draft renders correctly.",
            file=sys.stderr,
        )
    return body


def wait_until_live(url, timeout=900, interval=20):
    """Poll until the post URL returns 200 (GitHub Pages deploy takes a minute or two)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    return True
        except urllib.error.URLError:
            pass
        print(f"  waiting for {url} to go live...")
        time.sleep(interval)
    return False


def create_email(subject, body, canonical_url, send):
    payload = {
        "subject": subject,
        "body": body,
        "canonical_url": canonical_url,
        "status": "about_to_send" if send else "draft",
    }
    headers = {
        "Authorization": f"Token {os.environ['BUTTONDOWN_API_KEY']}",
        "Content-Type": "application/json",
        "X-API-Version": API_VERSION,
        "User-Agent": USER_AGENT,
    }
    if send:
        # Buttondown requires this the first time an API key sends. Only set
        # when you've deliberately chosen BUTTONDOWN_MODE=send.
        headers["X-Buttondown-Live-Dangerously"] = "true"

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Buttondown API error {err.code}: {detail}") from err


def main(argv):
    dry_run = "--dry-run" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("No posts given; nothing to do.")
        return 0
    if MODE not in ("draft", "send"):
        print(
            f"BUTTONDOWN_MODE must be 'draft' or 'send', got '{MODE}'", file=sys.stderr
        )
        return 1
    if not dry_run and not os.environ.get("BUTTONDOWN_API_KEY"):
        print("BUTTONDOWN_API_KEY is not set.", file=sys.stderr)
        return 1

    failures = 0
    for path in paths:
        print(f"Processing {path}")
        try:
            front, body = parse_post(path)
            if front.get("newsletter") is False or front.get("published") is False:
                print("  skipped (newsletter: false / published: false)")
                continue
            subject = str(front.get("title") or "").strip()
            if not subject:
                raise ValueError("no title in front matter")

            url = post_url(path, front)
            body = prepare_body(body)
            if ADD_WEB_LINK:
                body = f"[Read on the web →]({url})\n\n{body}"

            send = MODE == "send"
            if dry_run:
                print(
                    f"  [dry run] mode={MODE} subject={subject!r}\n  canonical_url={url}"
                )
                print("  ---- body preview ----")
                print("  " + body[:600].replace("\n", "\n  "))
                continue

            if send and not wait_until_live(url):
                print(
                    "  WARNING: post never went live; creating a draft instead.",
                    file=sys.stderr,
                )
                send = False

            result = create_email(subject, body, url, send)
            print(
                f"  created email {result.get('id')} (status: {result.get('status')})"
            )
        except Exception as exc:  # keep going so one bad post doesn't block the rest
            failures += 1
            print(f"  ERROR: {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
