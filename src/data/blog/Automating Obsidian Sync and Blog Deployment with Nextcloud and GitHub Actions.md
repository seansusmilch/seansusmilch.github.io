---
author: Sean
pubDatetime: 2025-02-18T23:44:00Z
modDatetime: 2025-06-12T01:47:08.117Z
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
  - obsidian
  - file-synchronization
---
I recently set up a workflow that allows my Obsidian notes to automatically sync between devices and also update my blog without any manual intervention. This was accomplished using the **Remotely Save** plugin for Obsidian, a **Nextcloud WebDAV** connection, a **GitHub Action** that runs a **Python script** that syncs posts to the repository, and another action to **deploy to GitHub Pages**.

## Table of Contents

## Inspiration

This setup was inspired by [a video from NetworkChuck](https://youtu.be/dnE7c0ELEH8?si=YlK2PJ4si6hp_KzO), where he explored how to create a blog post pipeline, from markdown written in Obsidian to a live blog post on your site. His approach made it easy to write and publish directly from Obsidian, but I wanted to take it a step further by **adding automatic syncing across all my devices**.

Instead of just pulling blog posts from Obsidian, I wanted my **entire note-taking system** to be synced seamlessly across devices. That way, any edits I made whether for blog posts or general notes would always be up to date no matter where I was working.

## The Goals

⬜ Sync Obsidian notes across devices

⬜ Store notes in Nextcloud

⬜ Automatically update blog site with latest posts from Obsidian notes

⬜ ⭐BONUS: Allow the blog posts folder to be moved/renamed in the vault!


## 1. Syncing Obsidian Notes with Nextcloud

To keep my Obsidian notes synced across devices, I used the [Remotely Save](https://github.com/remotely-save/remotely-save) plugin. This plugin allows Obsidian to sync files via various backends. The one I'm interested for this is **WebDAV**, as **Nextcloud** provides a WebDAV endpoint by default.

> Sidenote: Originally, I wanted to sync my notes to GitHub. However, that proved to be a messy pain in the ass. It was just merge conflicts on top of merge conflicts. Sure, it might be a skill issue, but I want this setup to be as frictionless and hands off as possible. So I decided to switch to my already existing Nextcloud instance.

> Another Sidenote: I actually switched my main syncing solution to Syncthing! I use Syncthing in conjunction with Remotely Save and Nextcloud to keep this blog pipeline going. Perhaps in the future, I'll remove the dependency on Remotely Save, but for now, I'm happy. Read more about it [here](https://seansusmilch.github.io/posts/obsidian-syncthing-private-sync-guide/)
### Setting Up Remotely Save with Nextcloud

At a high level, this is what I did to achieve this.

1. Install the [Remotely Save](https://github.com/remotely-save/remotely-save) plugin in Obsidian.
2. Configure it to use **WebDAV** as the sync method.
3. Enter the WebDAV URL, username, and password of my Nextcloud instance.
4. Enable automatic syncing so that any changes in my Obsidian vault are pushed to Nextcloud.

> I highly suggest you back up your vault and read up on the [Remotely Save](https://github.com/remotely-save/remotely-save) docs before implementing this into your vault!!!

We now have the first half of our Obsidian to Blog pipeline!
![obsidian-to-blog-pipeline.png](@/assets/blog/obsidian-to-blog-pipeline.png)

With this setup, my notes are always up-to-date across devices without needing to rely on third-party cloud services like iCloud or Google Drive.

✅ Sync Obsidian notes across devices

✅ Store notes in Nextcloud

## 2. Automating Blog Updates with GitHub Actions

In order for us to achieve this part, we'll need some way to execute some scripts . What I ended up going with was a **GitHub Action** that runs a Python script to:

  1. **Fetch** posts from my Nextcloud WebDAV folder (where my Obsidian notes are stored).
  2. **Clone** those posts into a GitHub repository.
  3. **Push** the updated posts to the repository.
  4. **Trigger** another workflow to deploy to **GitHub Pages**

These components should complete our Obsidian to Blog pipeline!
![obsidian-to-blog-pipeline.png](@/assets/blog/obsidian-to-blog-pipeline.png)

### Sync Posts GitHub Action

[seansusmilch.github.io/.github/workflows/sync-posts.yaml](https://github.com/seansusmilch/seansusmilch.github.io/blob/main/.github/workflows/sync-posts.yaml)

The goal of this action is to fetch and process posts from our Obsidian vault via the WebDAV connection we're syncing to. This action runs on a cron schedule, but I can also execute it manually if I want to push an update through.

This action does the following:
1. Busy work
	1. Clone the blog repo
	2. Set up Python
	3. Set up rclone
2. Executes `scripts/sync-posts.py` (we'll get into this further)
3. Triggers a separate action to deploy to GitHub Pages

### Sync Posts Script

[seansusmilch.github.io/scripts/sync-posts.py](https://github.com/seansusmilch/seansusmilch.github.io/blob/main/scripts/sync-posts.py)

This script was adapted from Network Chuck's script . His version of the script covered processing images and markdown pretty well. However since he was running this script on his local pc, and this setup is running in a GH action, Some modifications were needed.

One feature that I recently added, and I'm pretty happy about, is the "marker" file approach to figuring out where your blog posts are in your Obsidian vault. 

What is this "marker" file approach? It's actually pretty simple.

#### Marker File

Let's say you are looking for a folder, but you want to be able to move that folder around. You want the name, as well as its parent folder to be able to change, while your script still being able to locate it. How do?

That's where a "marker" file can be useful.

The idea is that this marker file will live within the folder your script is interested in, and that it has a **unique** name. This allows your script to just glob an entire section of your filesystem looking for this unique filename. 

That's the approach I've taken with `sync-posts.py`. The function `find_posts_source()` recursively looks for the first file named `!BLOG_POSTS!.md`. Whenever it finds that file, the script knows that the parent folder is where all the blog posts are!

✅ ⭐BONUS: Allow the blog posts folder to be moved/renamed in the vault!

### Trigger Blog Deploy Action

[seansusmilch.github.io/.github/workflows/deploy-gh-pages.yaml](https://github.com/seansusmilch/seansusmilch.github.io/blob/main/.github/workflows/deploy-gh-pages.yaml)

This one actually took some digging into permissions to get going. The problem I was running into was that by default, commits generated by GH Actions are not allowed to execute other GH Actions.

A solution to this is to dispatch an event to your repo via the `actions/github-script` action. Here's a full snippet:

```yaml
  - name: Trigger Deploy Workflow
	if: steps.commit-action.outputs.changes_detected == 'true'
	uses: actions/github-script@v7
	with:
	  script: |
		github.rest.repos.createDispatchEvent({
		  owner: context.repo.owner,
		  repo: context.repo.repo,
		  event_type: 'publish-trigger',
		});
```

This will dispatch an event called `publish-trigger` to your GH repo, and any action listening for that event will fire. 

For your deploy action, you'll need to listen for this event by adding this snippet:

```yaml
on:
  ...
  # Trigger the workflow on a repository dispatch event of type 'publish-trigger'
  repository_dispatch:
    types: [publish-trigger]
```

This action handles the deployment of my markdown blog, which I created from a template called [satnaing/astro-paper](https://github.com/satnaing/astro-paper)

✅ Automatically update blog site with latest posts from Obsidian notes

## Final Thoughts

Welp, that completes our Obsidian to Blog pipeline!

![obsidian-to-blog-pipeline.png](@/assets/blog/obsidian-to-blog-pipeline.png)

This pipeline, leveraging **Obsidian's Remotely Save plugin**, **Nextcloud WebDAV**, and **GitHub Actions**, is my attempt at making note-taking and blogging easier for me. My primary goal of seamless syncing across devices and automated blog updates is now fully realized. It's incredibly satisfying to write in Obsidian, knowing my content is effortlessly synced and published without any manual intervention.

The setup is truly **frictionless** and **hands-off**, allowing me to focus entirely on content creation. The **"marker file"** approach for dynamically locating blog posts was a small but significant bonus, allowing me to reorganize my vault how I please.

Again, credit to Network Chuck and his [blog post](https://blog.networkchuck.com/posts/my-insane-blog-pipeline/) and [video](https://www.youtube.com/watch?v=dnE7c0ELEH8) for being a great inspiration and technical resource!

---

_If you'd like to see the specifics, feel free to look at the code on my GitHub repo [here](https://github.com/seansusmilch/seansusmilch.github.io)_
