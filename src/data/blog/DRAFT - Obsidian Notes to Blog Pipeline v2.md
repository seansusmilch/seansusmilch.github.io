---
author: Sean
pubDatetime: 2026-02-06T13:42:00Z
slug: obsidian-to-blog-pipeline-v2
title: Obsidian Notes to Blog Pipeline v2
description: My updated pipeline that brings my Obsidian notes to my blog automatically
featured: true
draft: true
tags:
  - obsidian
  - automation
  - syncthing
  - project
  - homelab
  - python
---
## Table of contents

This post lays out my new Obsidian to blog pipeline that re-architects it to a *push* strategy instead of the previous *pull* strategy. With my switch from RemotelySave to [Syncthing as my Obsidian syncing solution of choice](https://seansusmilch.github.io/posts/obsidian-syncthing-private-sync-guide/), I wanted to eliminate another dependency in my Obsidian to blog pipeline, Nextcloud. Removing this dependency, along with my experience setting up the old pipeline, resulted in a much smoother and simpler pipeline to keep my blog in sync with my Obsidian notes.

## Review

Before we get into the new, lets have a quick review of the old. My old stack can be summed up to this order of events:

My Device
1. Write blog post in Obsidian
2. Remotely Save plugin syncs file to Nextcloud

On Github
1. On schedule (twice a day)
2. Set up Nextcloud client (rclone)
3. Find anchor file `!BLOG_POSTS!.md` to find blog posts folder
4. Pull posts into repo
5. Process image links in markdown
6. Pull attached images into repo
7. Commit & push

My problems with this setup, especially after switching to Syncthing for my syncing needs, was that it depended on getting my notes into Nextcloud. This was nowhere near as convenient It was a clear next dependency to remove from the pipeline. Also, all the credentials to connect to my entire Nextcloud instance would be saved and used in GitHub

## What's The Next Solution? 

I originally thought of trying to refactor the existing GitHub action to connect to my Syncthing network, but after thinking about it for awhile, its a questionable architecture in terms of privacy. 

%% maybe do less of a privacy play or include that my previous setup had a big oversight %%
Think about it, your entire Obsidian vault would be copied onto a GH action runner, and the credentials to do it would be saved in GitHub. Since I keep my blog posts in the same vault as my personal notes, I said no thanks to this strategy. Also, it has never been done before (to my knowledge) and I would be paving the way in getting Syncthing to work in a github action.

I acknowledge that my previous setup where GitHub Actions would connect to my notes via Next Cloud wasnt any better and was probably a big oversight in terms of privacy and opsec. 

This is when I realized a push strategy coming from a machine that I control would be preferred.

## The Push Strategy

The push strategy comes with many advantages over the previous pull strategy.

- I can run it on an existing server that's on 24 7.
- I won't need to waste gitHub Action runs that result in no changes
- gitHub will never have full access to my notes like it did with the pull strategy.

%% add a graphic here to explain the flow visually %%
So the basic idea is this. I write my notes on my laptop in Obsidian. With Syncthing, my notes get synced up to my always on server. Then, on a schedule, a script that takes care of the pushing gets run.

At a high level, that script is responsible for the following: 

1. Set up git credentials and clone blog repo 
2. Find anchor file within vault (`! BLOG_POSTS!.md`)
3. Sync obsidian blog post notes to blog repo 
4. In each post convert image wikilinks to markdown links
5. Sync images that are referenced in posts to blog repo
6. Commit and push

It's pretty similar to the script from the pull strategy, except we are dealing with git instead of nextcloud

## Technical Execution

Now that we have a basic understanding of what we are trying to do, let's get into the execution of setting up this workflow.

As I've talked about in my post about [Syncthing and Obsidian](https://seansusmilch.github.io/posts/obsidian-syncthing-private-sync-guide/), I have a VM in Oracle Cloud that is running 24.7, and acting as a persistent Syncthing node. This makes it a perfect place to have this script run on a schedule.

Since I'm running Coolify on this VM, I want to be able to view logs and control deploys, and set the scheduled sync job through Coolify's WebUI. This means that dockerizing my solution would offer me the best experience.

So now the idea is this: Have a docker container running, idling, until Coolify's scheduling system attaches and runs the script to push posts up to the blog repo.
### Using Docker as an Always on Machine

This was my first challenge. I've never had a docker container just running as another "machine" to attach to. The entire point of docker to my understanding is one process per container. No process, no container.

I don't think this is an *ideal* use of docker, but that's not important to me right now, getting something working is.

The solution to this is pretty simple. Just have your container sleep indefinitely 😅

```Dockerfile
FROM alpine

CMD ["sleep", "infinity"]
```

This allows the container to stay running and allow me to attach to it to figure out what I all need to get this working.

After attaching to the container with `docker exec -it <container name> /bin/sh`, I began setting up my script and noting down all the requirements for smooth execution:

- Rsync, Python and Git installed
- Various env vars
	- Repo url
	- Git username, email, personal access token
	- Source dirs and destination dirs
	- Anchor filename
	- Astro image link prefix
- Sync posts script (with executable flag!)

Here's my final [`Dockerfile`](https://github.com/seansusmilch/seansusmilch.github.io/blob/637b46fc48201cc9e767b1cd990bdc7b01925cef/sync-posts/Dockerfile) that has everything I needs

```Dockerfile
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

RUN chmod +x sync-posts.py

CMD ["sleep", "infinity"]
```

Now it's ready to go live in Coolify!
### Coolify Setup

Okay the truth is, I set this part up before doing the above. I was just pushing changes to the Dockerfile and letting Coolify deploy, then used their integrated terminal to figure out what needed to be done for this sync posts script.

The build setup was simple. In my blog repo, I put this posts syncing project in a new folder `/sync-posts`, then pointed Coolify to watch for any changes in that dir, and pointed it at that Dockerfile.

![obsidian-blog-2-coolify-build.png](@/assets/blog/obsidian-blog-2-coolify-build.png)

Once the container was up and running in Coolify, and I confirmed that all the requirements for the script were in place, and logging in, running the script with `/app/sync-posts.py` (multiple times) would all work as expected, I moved on to setting up the schedule. I set it up to run hourly.

![obsidian-blog-2-coolify-schedule.png](@/assets/blog/obsidian-blog-2-coolify-schedule.png)

