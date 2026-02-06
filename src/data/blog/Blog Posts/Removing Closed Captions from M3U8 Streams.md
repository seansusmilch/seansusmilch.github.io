---
author: Sean
pubDatetime: 2025-02-17T22:48:00Z
slug: removing-closed-captions-from-m3u8-streams
title: Removing Closed Captions from M3U8 Streams w/ FFmpeg
description: Using Threadfin and FFmpeg to remove subpar captions in live broadcasts
featured: false
draft: false
tags:
  - linux
  - media-server
  - live-stream
  - ffmpeg
  - threadfin
---

![[../assets/image_sports-broadcast-captions.png]]
I recently ran into some m3u8 live streams that had captions embedded in the stream. They were pretty much useless, missing every other word and not even in sync. I decided to filter out the captions stream...but how do??

For context, I'm using [Threadfin](https://github.com/Threadfin/Threadfin) to proxy my streams to Emby and Jellyfin. A lot of fine tuning had to be done to get where I'm at, but it's finally working well!

- ## Removing the Captions

  Threadfin, is the place where FFMPEG gets to remove the captions. The key is adding this option to your FFmpeg options.

  ```
  -bsf:v filter_units=remove_types=6
  ```

  An FFmpeg wiki post [here](https://trac.ffmpeg.org/wiki/HowToExtractAndRemoveClosedCaptions) showcases this option. This was a struggle for me to find since it's often assumed that subtitles or captions are in separate streams in the media container. However, for live broadcasts, they're actually inside the video stream.

- ## Threadfin FFmpeg Options

  This is the FFmpeg options that I've landed on that work fairly well. I've formatted it nicely just for this post 😎

  ```
  -hide_banner
  -loglevel error
  -fflags +genpts+discardcorrupt
  -i [URL]
  -map 0:v
  -map 0:a?
  -bsf:v filter_units=remove_types=6
  -c copy
  -f mpegts
  -copyts
  -reconnect 1
  -reconnect_streamed 1
  -reconnect_on_network_error 1
  -reconnect_delay_max 10
  -fflags +nobuffer
  pipe:1
  ```

  If you find any FFmpeg options that could be improved, drop a comment below
