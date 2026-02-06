#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path

IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "webp"]
TEMP_REPO_DIR = Path("/tmp/blog-repo")
COMMIT_MESSAGE = "Update blog posts"


class Config:
    def __init__(self):
        self.source_dir = Path(os.environ["SOURCE_DIR"])
        self.anchor_filename = os.environ["ANCHOR_FILENAME"]
        self.repo_url = os.environ["REPO_URL"]
        self.gh_pat = os.environ["GH_PAT"]
        self.dest_posts = os.environ["DEST_POSTS"]
        self.dest_attachments = os.environ["DEST_ATTACHMENTS"]
        self.attachment_prefix = os.environ["ATTACHMENT_PREFIX"]
        self.git_email = os.environ["GIT_EMAIL"]
        self.git_name = os.environ["GIT_NAME"]


def run_command(args, cwd=None, check=True):
    return subprocess.run(args, cwd=cwd, check=check)


def log(message):
    print(message)


def clone_and_setup_repo(config):
    auth_url = config.repo_url.replace("https://", f"https://{config.gh_pat}@")

    run_command(
        ["git", "clone", "--filter=blob:none", "--sparse", auth_url, TEMP_REPO_DIR]
    )
    run_command(["git", "sparse-checkout", "init"], cwd=TEMP_REPO_DIR)
    run_command(
        ["git", "sparse-checkout", "set", config.dest_posts, config.dest_attachments],
        cwd=TEMP_REPO_DIR,
    )

    log(f"Repository cloned and setup in {TEMP_REPO_DIR}")

    return TEMP_REPO_DIR


def find_anchor_file(config):
    for f in config.source_dir.rglob(config.anchor_filename):
        log(f"Anchor file found in {f}")
        return f
    raise FileNotFoundError(
        f"Anchor file {config.anchor_filename} not found in {config.source_dir}"
    )


def sync_posts(config, anchor_path, repo_dir):
    source_path = config.source_dir / anchor_path.parent.name
    dest_path = repo_dir / config.dest_posts

    rsync_result = run_command(
        [
            "rsync",
            "-av",
            "--delete",
            "--exclude",
            config.anchor_filename,
            f"{source_path}/",
            f"{dest_path}/",
        ]
    )
    log(
        f"Rsync result: {rsync_result.returncode} {rsync_result.stdout} {rsync_result.stderr}"
    )

    return dest_path


def process_images_in_posts(posts_dir, config):
    images = set()
    image_pattern = r"\[\[([^]]*\.(?:{}))\]\]".format("|".join(IMAGE_EXTENSIONS))

    for post_file in posts_dir.glob("*.md"):
        content = post_file.read_text()

        def replace_image(match):
            src = match.group(1)
            images.add(src)
            image_path = Path(src)
            markdown_image = f"[{image_path.name}]({config.attachment_prefix}/{image_path.name.replace(' ', '%20')})"
            log(f"Replacing image [[{src}]] with {markdown_image}")
            return markdown_image

        content = re.sub(image_pattern, replace_image, content)
        post_file.write_text(content)

    log(f"Images processed in {posts_dir}")
    return images


def sync_images(images, anchor_path, repo_dir, config):
    dest_attachments_path = repo_dir / config.dest_attachments
    anchor_dir = anchor_path.parent

    for img in images:
        src_img = (anchor_dir / img).resolve()
        log(f"Syncing image {src_img} to {dest_attachments_path}")
        if src_img.exists():
            run_command(["rsync", "-av", str(src_img), str(dest_attachments_path)])


def commit_and_push(repo_dir, config, no_commit=False):
    if no_commit:
        log("Skipping commit due to --no-commit flag")
        return

    run_command(["git", "add", "."], cwd=repo_dir)

    result = run_command(
        ["git", "diff", "--cached", "--quiet"], cwd=repo_dir, check=False
    )
    if result.returncode == 0:
        log("No changes to commit")
        return

    run_command(["git", "config", "user.email", config.git_email], cwd=repo_dir)
    run_command(["git", "config", "user.name", config.git_name], cwd=repo_dir)
    run_command(["git", "commit", "-m", COMMIT_MESSAGE], cwd=repo_dir)
    run_command(["git", "push", "origin", "HEAD"], cwd=repo_dir)


def cleanup_repo(repo_dir, no_cleanup=False):
    if no_cleanup:
        log(f"Skipping cleanup, repo left at {repo_dir}")
        return

    if repo_dir.exists():
        shutil.rmtree(repo_dir)
        log(f"Repository cleaned up in {repo_dir}")


def main():
    parser = argparse.ArgumentParser(description="Sync blog posts and images")
    parser.add_argument(
        "--no-commit", action="store_true", help="Skip committing changes"
    )
    parser.add_argument(
        "--no-cleanup", action="store_true", help="Leave repo in tmp folder"
    )
    args = parser.parse_args()

    config = Config()

    repo_dir = clone_and_setup_repo(config)
    anchor_path = find_anchor_file(config)
    posts_dir = sync_posts(config, anchor_path, repo_dir)
    images = process_images_in_posts(posts_dir, config)
    sync_images(images, anchor_path, repo_dir, config)
    commit_and_push(repo_dir, config, no_commit=args.no_commit)
    cleanup_repo(repo_dir, no_cleanup=args.no_cleanup)


if __name__ == "__main__":
    main()
