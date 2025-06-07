---
author: Sean
pubDatetime: 2025-02-18T23:44:00Z
slug: obsidian-sync-and-blog
title: Automating Obsidian Sync and Blog Deployment with Nextcloud and GitHub Actions
description: How I’m able to write my blog posts in Obsidian and have them automatically show up here!
featured: false
draft: false
tags:
  - automation
  - python
  - homelab
  - project
---
I recently set up a workflow that allows my Obsidian notes to automatically sync between devices and also update my blog without any manual intervention. This was accomplished using the **Remotely Save** plugin for Obsidian, a **Nextcloud WebDAV** connection, a **GitHub Action** that runs a **Python script** that syncs posts to the repository, and another action to **deploy to GitHub Pages**.
## Table of contents

## Inspiration

This setup was inspired by [a video from **NetworkChuck**](https://youtu.be/dnE7c0ELEH8?si=YlK2PJ4si6hp_KzO), where he explored how to create a blog post pipeline, from markdown written in Obsidian to a live blog post on your site. His approach made it easy to write and publish directly from Obsidian, but I wanted to take it a step further by **adding automatic syncing across all my devices**.

Instead of just pulling blog posts from Obsidian, I wanted my **entire note-taking system** to be synced seamlessly across devices. That way, any edits I made whether for blog posts or general notes would always be up to date no matter where I was working.

## How It Works

### 1. Syncing Obsidian Notes with Nextcloud

To keep my Obsidian notes synced across devices, I used the [Remotely Save](https://github.com/remotely-save/remotely-save) plugin. This plugin allows Obsidian to sync files via various backends, including **WebDAV**, which I used to connect to my **Nextcloud** instance.
> Originally, I wanted to sync my notes to GitHub. However, that proved to be a messy pain in the ass. So I decided to switch to my already existing Nextcloud instance.

#### Steps to Set Up Remotely Save with Nextcloud

1. Install the **Remotely Save** plugin in Obsidian.
2. Configure it to use **WebDAV** as the sync method.
3. Enter the WebDAV URL of my Nextcloud instance.
4. Provide authentication credentials.
5. Enable automatic syncing so that any changes in my Obsidian vault are pushed to Nextcloud.

With this setup, my notes are always up-to-date across devices without needing to rely on third-party cloud services like iCloud or Google Drive.

### 2. Automating Blog Updates with GitHub Actions

Since my blog posts are stored as Markdown files in my Obsidian vault, I wanted a way to **automatically update my blog** whenever I made changes to my notes. What I ended up going with was a **GitHub Action** that runs a Python script to:

  1. **Fetch** posts from my Nextcloud WebDAV folder (where my Obsidian notes are stored). 
  2. **Clone** those posts into a GitHub repository.  
  3. **Push** the updated posts to the repository.
  4. **Trigger** another workflow to deploy to **GitHub Pages**

These components should make up the Obsidian to blog pipeline!
![obsidian-to-blog-pipeline.png](@/assets/blog/obsidian-to-blog-pipeline.png)
#### See the specifics of this in my blog's GitHub repo!

[seansusmilch/seansusmilch.github.io](https://github.com/seansusmilch/seansusmilch.github.io)

I have a GitHub workflow called [Sync Posts](https://github.com/seansusmilch/seansusmilch.github.io/actions/workflows/sync-posts.yaml) that does the following:

- This sets up an `rclone` remote to my WebDAV endpoint
	- Endpoint and auth set through GitHub environment variables
- Then runs a Python script [scripts/sync-posts.py](https://github.com/seansusmilch/seansusmilch.github.io/blob/main/scripts/sync-posts.py) that will sync posts to the repo
	- The path in my Obsidian vault is set through a GitHub environment variable
- Then triggers the [Deploy to GitHub Pages](https://github.com/seansusmilch/seansusmilch.github.io/actions/workflows/deploy-gh-pages.yaml) workflow
- The blog template I used is [Astro Paper](https://github.com/satnaing/astro-paper)

## The Result

With this setup:

 - [x] My **Obsidian notes** stay synced across all my devices via **Nextcloud WebDAV**.
 - [x] My **blog updates automatically** whenever I edit posts in Obsidian.
 - [x] **No manual intervention** is needed to deploy new posts.

This workflow saves me time and ensures that my Obsidian notes are a “source of truth” so to speak.

### What can be better?

This setup does have at least one flaw in my opinion. That is, once you have all this set up you can't move your blog posts around or rename folders in your Obsidian vault. If you do so, you'd have to update the environment variables in your GitHub repo 👎

That's why when I come back to this, I'm going to try out an idea to resolve this problem.
Instead of specifying a path, we could specify a special filename (ex. `!BLOG_POSTS!`) which `sync-posts.py` could then search for within your vault in order to find all your blog posts! 👍

---
_If you'd like to see the specifics, feel free to look at the code on my GitHub repo [here](https://github.com/seansusmilch/seansusmilch.github.io)_