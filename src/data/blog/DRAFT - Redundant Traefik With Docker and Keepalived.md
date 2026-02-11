---
author: Sean
pubDatetime: 2026-02-11T00:02:00Z
slug: redundant-traefik-with-docker-keepalived
title: Redundant Traefik with Docker and Keepalived
description: Here's a look at how I was able to set up redundant traefik as my reverse proxy with Docker and keepalived.
featured: true
draft: true
tags:
  - reverse-proxy
  - traefik
  - docker
  - keepalived
  - redundancy
---
## Table of contents

But kubernetes exists! But docker swarm exists! Nah I rolled it myself 😤

Wanted to learn traefik for the longest time. Didn't want to switch all my vms to docker swarm or kubernetes. Ended up having a pretty decent setup with redundancy (tested!!!) and synced traefik configs via github instead of via tags meaning the traefik instances are completely decoupled from the rest of my homelab services