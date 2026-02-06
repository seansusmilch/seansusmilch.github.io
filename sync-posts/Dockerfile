FROM alpine

ENV SOURCE_DIR=/data
ENV ANCHOR_FILENAME=!BLOG_POSTS!.md
ENV REPO_URL=
ENV GH_PAT=
ENV DEST_POSTS=src/data/blog
ENV DEST_ATTACHMENTS=src/assets/blog
ENV ATTACHMENT_PREFIX=@/assets/blog
ENV GIT_EMAIL=action@github.com
ENV GIT_NAME="Sync Posts Bot"

WORKDIR /app

RUN apk add --no-cache rsync python3 git

COPY . .

CMD ["sleep", "infinity"]
