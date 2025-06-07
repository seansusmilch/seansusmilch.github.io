import os
import re
import subprocess
from pathlib import Path

# Paths
source_base_dir = os.getenv("SOURCE_BASE_DIR", "/Obsidian")
source_special_filename = os.getenv("SOURCE_SPECIAL_FILENAME", "!BLOG_POSTS!.md")

dest_posts = os.getenv("DEST_POSTS", "src/data/blog")
dest_attachments = os.getenv("DEST_ATTACHMENTS", "src/assets/blog")
attachment_prefix = os.getenv("ATTACHMENT_PREFIX", "@/assets/blog")


def sync_markdown(cloud: Path, local: Path):
    # rclone sync "nc:${SOURCE_POSTS}" "${DEST_POSTS}"
    print(f"MARKDOWN: Syncing markdown from {cloud} to {local}")
    subprocess.Popen(
        [
            "rclone",
            "sync",
            "--exclude",
            source_special_filename,
            f"nc:{Path(cloud).as_posix()}",
            Path(local).as_posix(),
        ]
    ).wait()


def sync_image(cloud: Path, local: Path):
    print(f"IMAGES: Syncing image from {cloud} to {local}")
    subprocess.Popen(
        ["rclone", "sync", f"nc:{Path(cloud).as_posix()}", Path(local).as_posix()]
    ).wait()


def find_posts_source(root: Path) -> Path:
    result = subprocess.run(
        [
            "rclone",
            "lsf",
            "--recursive",
            "--files-only",
            "--include",
            source_special_filename,
            f"nc:{Path(root).as_posix()}",
        ],
        capture_output=True,
        text=True,
        check=True,
        encoding="utf8",
    )
    if result.returncode != 0:
        raise Exception(f"Error: {result.stderr}")

    # output is '' if not found
    lines = result.stdout.splitlines()

    if len(lines) == 0:
        return None

    if len(lines) > 1:
        print(f"WARNING: Multiple special files found: {lines}")

    special_file = Path(lines[0])
    return special_file.parent


def main():
    # find where the posts are stored
    posts_source = find_posts_source(Path(source_base_dir))
    if posts_source is None:
        raise Exception(f"No posts found in {source_base_dir}")

    sync_markdown(Path(source_base_dir) / posts_source, Path(dest_posts))

    # Step 1: Process each markdown file in the posts directory
    for filepath in Path(dest_posts).rglob("*.md"):
        print(f"IMAGES: Processing {filepath}...")
        with open(filepath, "r", encoding="utf8") as file:
            content = file.read()

        # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
        images = re.findall(r"\[\[([^]]*\.(?:png|jpg|jpeg|gif|webp))\]\]", content)

        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            image_path = Path(image)
            markdown_image = f"[{image_path.name}]({attachment_prefix}/{image_path.name.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)

            # Step 4: Copy the image to the Hugo static/images directory if it exists
            image_source = Path(source_base_dir) / image
            sync_image(image_source, dest_attachments)

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf8") as file:
            file.write(content)

    print("Markdown files processed and images copied successfully.")


if __name__ == "__main__":
    main()
