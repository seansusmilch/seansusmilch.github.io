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

## The Next Solution

I originally thought of trying to refactor the existing GitHub action to connect to my Syncthing network, but after thinking about it for awhile, its a questionable architecture in terms of privacy. 

Think about it, your entire Obsidian vault would be copied onto a GH action runner, and the credentials to do it would be saved in GitHub. Since I keep my blog posts in the same vault as my personal notes, I said no thanks to this strategy. Also, it has never been done before (to my knowledge) and I would be paving the way in getting Syncthing to work in a github action.

