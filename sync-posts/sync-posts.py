#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path
import re


SOURCE_DIR = Path(os.environ["SOURCE_DIR"])
ANCHOR_FILENAME = os.environ["ANCHOR_FILENAME"]
REPO_URL = os.environ["REPO_URL"]
GH_PAT = os.environ["GH_PAT"]
DEST_POSTS = os.environ["DEST_POSTS"]
DEST_ATTACHMENTS = os.environ["DEST_ATTACHMENTS"]
ATTACHMENT_PREFIX = os.environ["ATTACHMENT_PREFIX"]
GIT_EMAIL = os.environ["GIT_EMAIL"]
GIT_NAME = os.environ["GIT_NAME"]


def clone_and_setup_repo(repo_url, gh_pat, dest_posts, dest_attachments):
    REPO_DIR = Path("/tmp/blog-repo")
    auth_url = repo_url.replace("https://", f"https://{gh_pat}@")

    subprocess.run(
        ["git", "clone", "--filter=blob:none", "--sparse", auth_url, REPO_DIR],
        check=True,
    )
    subprocess.run(["git", "sparse-checkout", "init"], cwd=REPO_DIR, check=True)
    subprocess.run(
        ["git", "sparse-checkout", "set", dest_posts, dest_attachments],
        cwd=REPO_DIR,
        check=True,
    )

    print(f"Repository cloned and setup in {REPO_DIR}")

    return REPO_DIR


def find_anchor_file(source_dir, anchor_filename):
    for f in source_dir.rglob(anchor_filename):
        print(f"Anchor file found in {f}")
        return f
    raise FileNotFoundError(f"Anchor file {anchor_filename} not found in {source_dir}")


def sync_posts(source_dir, anchor_path, repo_dir, dest_posts):
    dest_posts_path = repo_dir / dest_posts
    rsync_result = subprocess.run(
        [
            "rsync",
            "-av",
            "--delete",
            "--exclude",
            ANCHOR_FILENAME,
            str(source_dir / anchor_path.parent.name) + "/",
            str(dest_posts_path) + "/",
        ],
        check=True,
    )
    print(
        f"Rsync result: {rsync_result.returncode} {rsync_result.stdout} {rsync_result.stderr}"
    )
    return dest_posts_path


def process_images_in_posts(posts_dir, attachment_prefix):
    images = set()

    for post_file in posts_dir.glob("*.md"):
        content = post_file.read_text()

        def replace_image(match):
            src = match.group(1)
            images.add(src)
            image_path = Path(src)
            markdown_image = f"[{image_path.name}]({attachment_prefix}/{image_path.name.replace(' ', '%20')})"
            print(f"Replacing image [[{src}]] with {markdown_image}")
            return markdown_image

        content = re.sub(
            r"\[\[([^]]*\.(?:png|jpg|jpeg|gif|webp))\]\]", replace_image, content
        )
        post_file.write_text(content)

    print(f"Images processed in {posts_dir}")
    return images


def sync_images(images, anchor_path, repo_dir, dest_attachments):
    dest_attachments_path = repo_dir / dest_attachments
    anchor_dir = anchor_path.parent

    for img in images:
        src_img = (anchor_dir / img).resolve()
        print(f"Syncing image {src_img} to {dest_attachments_path}")
        if src_img.exists():
            subprocess.run(
                ["rsync", "-av", str(src_img), str(dest_attachments_path)], check=True
            )


def commit_and_push(repo_dir):
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)

    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo_dir)
    if result.returncode == 0:
        print("No changes to commit")
        return

    subprocess.run(
        ["git", "config", "user.email", GIT_EMAIL],
        cwd=repo_dir,
        check=True,
    )
    subprocess.run(["git", "config", "user.name", GIT_NAME], cwd=repo_dir, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Update blog posts"], cwd=repo_dir, check=True
    )
    subprocess.run(["git", "push", "origin", "HEAD"], cwd=repo_dir, check=True)


def cleanup_repo(repo_dir):
    import shutil

    if repo_dir.exists():
        shutil.rmtree(repo_dir)
        print(f"Repository cleaned up in {repo_dir}")


def main():
    repo_dir = clone_and_setup_repo(REPO_URL, GH_PAT, DEST_POSTS, DEST_ATTACHMENTS)

    anchor_path = find_anchor_file(SOURCE_DIR, ANCHOR_FILENAME)

    posts_dir = sync_posts(SOURCE_DIR, anchor_path, repo_dir, DEST_POSTS)

    images = process_images_in_posts(posts_dir, ATTACHMENT_PREFIX)

    sync_images(images, anchor_path, repo_dir, DEST_ATTACHMENTS)

    commit_and_push(repo_dir)

    cleanup_repo(repo_dir)


if __name__ == "__main__":
    main()
