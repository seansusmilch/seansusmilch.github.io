# Sync Posts Container

This container syncs blog posts from a source directory to a remote blog repository.

## Usage

1. Log in to the running container
2. Run the sync-posts script with required environment variables

## Environment Variables

- `SOURCE_DIR` - Source directory containing posts
- `ANCHOR_FILENAME` - Anchor file to locate the posts directory
- `REPO_URL` - Git repository URL
- `GH_PAT` - GitHub Personal Access Token
- `DEST_POSTS` - Destination posts path in repo
- `DEST_ATTACHMENTS` - Destination attachments path in repo
- `ATTACHMENT_PREFIX` - Attachment prefix for image links
- `GIT_EMAIL` - Git commit email (default: action@github.com)
- `GIT_NAME` - Git commit username (default: Sync Posts Bot)

## Scheduling

This container is intended to be run on a schedule via cron job on a Docker host.

Example cron entry (runs daily at 2am):
```
0 2 * * * docker exec -e SOURCE_DIR=... -e ANCHOR_FILENAME=... sync-posts /sync-posts/sync-posts.py
```
