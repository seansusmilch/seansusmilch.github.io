import os
import re
from subprocess import Popen
from pathlib import Path

# Paths
source_posts = os.getenv('SOURCE_POSTS', '/Obsidian/Efforts/07 ✍️ Blog/Posts')
source_base_dir = os.getenv('SOURCE_ATTACHMENTS', '/Obsidian')

dest_posts = os.getenv('DEST_POSTS', 'src/content/blog')
dest_attachments = os.getenv('DEST_ATTACHMENTS', 'src/assets/blog')
attachment_prefix = '@/assets/blog'

def sync_markdown(cloud:Path, local:Path):
    # rclone sync "nc:${SOURCE_POSTS}" "${DEST_POSTS}"
    Popen(['rclone', 'sync', f'nc:{Path(cloud).as_posix()}', Path(local).as_posix()]).wait()

def sync_image(cloud:Path, local:Path):
    Popen(['rclone', 'sync', f'nc:{Path(cloud).as_posix()}', Path(local).as_posix()]).wait()


sync_markdown(Path(source_posts), Path(dest_posts))

# Step 1: Process each markdown file in the posts directory
for filepath in Path(dest_posts).rglob("*.md"):
    print(f"Processing {filepath}...")
    with open(filepath, "r", encoding='utf8') as file:
        content = file.read()
    
    # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
    images = re.findall(r'\[\[([^]]*\.(?:png|jpg|jpeg|gif|webp))\]\]', content)
    
    # Step 3: Replace image links and ensure URLs are correctly formatted
    for image in images:
        # Prepare the Markdown-compatible link with %20 replacing spaces
        image_path = Path(image)
        markdown_image = f"[{image_path.name}]({attachment_prefix}/{image_path.name.replace(' ', '%20')})"
        content = content.replace(f"[[{image}]]", markdown_image)
        
        # Step 4: Copy the image to the Hugo static/images directory if it exists
        image_source = Path(source_base_dir) / image
        print(image_source)
        sync_image(image_source, dest_attachments)
        

    # Step 5: Write the updated content back to the markdown file
    with open(filepath, "w", encoding='utf8') as file:
        file.write(content)

print("Markdown files processed and images copied successfully.")
