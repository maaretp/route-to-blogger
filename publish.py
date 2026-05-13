#!/usr/bin/env python3
"""Publish new/changed markdown posts (with images) to Blogger.

Required environment variables:
  GOOGLE_CLIENT_ID      — Google OAuth2 client ID
  GOOGLE_CLIENT_SECRET  — Google OAuth2 client secret
  GOOGLE_REFRESH_TOKEN  — OAuth2 refresh token (run get_refresh_token.py once)
  BLOGGER_BLOG_URL      — Full URL of the Blogger blog
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

POSTS_DIR = Path("posts")
PUBLISHED_FILE = POSTS_DIR / ".published.json"
BLOGGER_BLOG_URL = os.environ["BLOGGER_BLOG_URL"]
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/blogger",
    "https://www.googleapis.com/auth/drive.file",
]


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def get_credentials() -> Credentials:
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=GOOGLE_SCOPES,
    )
    creds.refresh(Request())
    return creds


def get_blog_id(service) -> str:
    blog = service.blogs().getByUrl(url=BLOGGER_BLOG_URL).execute()
    return blog["id"]


# ---------------------------------------------------------------------------
# Image upload
# ---------------------------------------------------------------------------

def _resolve_image_path(ref: str, search_dir: Path) -> Path | None:
    """Return the local path for an image reference, trying alt extensions."""
    candidate = search_dir / ref
    if candidate.exists():
        return candidate
    # The ref may have the wrong extension (e.g. .jpg but file is .png)
    stem = Path(ref).stem
    for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        alt = search_dir / f"{stem}{ext}"
        if alt.exists():
            return alt
    return None


def upload_to_drive(image_path: Path, drive_service) -> str:
    """Upload image to Google Drive, make it publicly readable, return direct URL."""
    _MIME = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime = _MIME.get(image_path.suffix.lower(), "image/png")
    media = MediaFileUpload(str(image_path), mimetype=mime, resumable=False)
    uploaded = (
        drive_service.files()
        .create(body={"name": image_path.name}, media_body=media, fields="id")
        .execute()
    )
    file_id = uploaded["id"]
    drive_service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
    ).execute()
    return f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"


# ---------------------------------------------------------------------------
# Markdown processing
# ---------------------------------------------------------------------------

def process_markdown(md_file: Path, drive_service) -> tuple[str, str]:
    """Return (title, html_body) for a markdown file, uploading images."""
    content = md_file.read_text(encoding="utf-8")

    # Extract title from the first H1 heading
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_file.stem

    # Upload local images to Google Drive and replace refs with public URLs
    image_dir = md_file.parent

    def replace_image(m: re.Match) -> str:
        alt_text = m.group(1)
        ref = m.group(2)
        if ref.startswith(("http://", "https://")):
            return m.group(0)  # already remote, leave as-is
        local = _resolve_image_path(ref, image_dir)
        if local is None:
            print(f"  Warning: image '{ref}' not found — embedding as-is", file=sys.stderr)
            return m.group(0)
        print(f"  Uploading {local.name} to Google Drive …")
        url = upload_to_drive(local, drive_service)
        return f"![{alt_text}]({url})"

    content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, content)

    html_body = markdown.markdown(
        content,
        extensions=["extra", "nl2br"],
    )
    return title, html_body


# ---------------------------------------------------------------------------
# State tracking
# ---------------------------------------------------------------------------

def load_published() -> dict:
    if PUBLISHED_FILE.exists():
        return json.loads(PUBLISHED_FILE.read_text(encoding="utf-8"))
    return {}


def save_published(data: dict) -> None:
    PUBLISHED_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def get_changed_posts() -> list[Path]:
    """Return posts/*.md files added or modified in the latest push."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACM", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        # Likely an initial commit with no parent; publish everything
        return list(POSTS_DIR.glob("*.md"))

    changed = result.stdout.strip().splitlines()
    posts = [
        Path(f)
        for f in changed
        if f.startswith("posts/") and f.endswith(".md")
    ]
    if not posts:
        # Fallback: publish all posts (useful for manual reruns)
        return list(POSTS_DIR.glob("*.md"))
    return posts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    changed = get_changed_posts()
    if not changed:
        print("No changed posts found.")
        return

    print(f"Posts to process: {[str(p) for p in changed]}")

    creds = get_credentials()
    blogger_service = build("blogger", "v3", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    blog_id = get_blog_id(blogger_service)
    published = load_published()

    for md_file in changed:
        if not md_file.exists():
            print(f"Skipping {md_file} (file not present)")
            continue

        print(f"\nProcessing {md_file} …")
        title, html_body = process_markdown(md_file, drive_service)
        post_key = str(md_file)

        if post_key in published:
            post_id = published[post_key]
            blogger_service.posts().update(
                blogId=blog_id,
                postId=post_id,
                body={"title": title, "content": html_body},
            ).execute()
            print(f"  Updated post: '{title}'")
        else:
            result = blogger_service.posts().insert(
                blogId=blog_id,
                body={"title": title, "content": html_body},
            ).execute()
            published[post_key] = result["id"]
            print(f"  Created post: '{title}' (id={result['id']})")

    save_published(published)
    print("\nDone. Remember to commit posts/.published.json.")


if __name__ == "__main__":
    main()
