---
author: Sean
pubDatetime: 2025-07-14T01:18:00Z
slug: how-i-figure-out-what-to-delete
title: Making Unwatched Media Walk the Plank
description: A showcase of a tool I built to help me figure out what to delete from my server when I need to clear up some space
featured: true
draft: true
tags:
  - showcase
  - nextjs
---
### Least Watched: Conquering the Unwatched Mountain in My Homelab

Welp, if you're anything like me, you've probably got a mountain of digital content you've accumulated over the years. Movies, TV shows, Linux ISOs (😉) – they just pile up, consuming gigabyte after gigabyte on your drives. For us "data hoarders," it's easy to forget what’s even in there, let alone what’s been watched. This isn't just about digital clutter; it leads to **wasted storage space**, and trust me, it can cause critical issues. I literally **ran out of space on zhydra**, and that caused my Nextcloud instance to completely stop working! Talk about a messy pain in the ass!

That headache, and the constant need for better alerts and clean-up tools, was the kick in the pants I needed. My goal? To finally get a handle on this "unwatched mountain" and deal with it **"whenever the drives fill up"**.

Enter **Least Watched**. This project is my attempt to help users (and myself) identify and manage unwatched or least-watched content in their media libraries. It’s designed to provide a **stable, easy-to-use web interface** to analyze watch data from services like Emby, Sonarr, and Radarr.

#### The Challenge: Why Manual Management Sucks

Seriously, trying to manually sift through hundreds or thousands of movies and TV shows to figure out what's truly unwatched? Forget about it. It’s **impractical for large libraries**. Content gets added, then just sits there, never viewed, just eating up valuable disk space. It's not just about freeing up storage; it's also about curating your library and rediscovering cool stuff you completely forgot you owned. That’s where the automation comes in, making it a truly **frictionless and hands-off** process.

#### How "Least Watched" Works: The Core Guts

"Least Watched" is a sophisticated media management application that pulls data from your existing media platforms. Here's the high-level view of how it operates:

- **Data Collection & Integration:** It connects directly to your media ecosystem:
    - **Emby:** This is the primary source for media library info. It uses Emby’s Playback Reporting plugin and some custom SQL queries to efficiently grab that viewing history data.
    - **Sonarr (TV Shows):** Grabs all the TV show metadata, including file sizes and paths. It’s also set up for automated show management.
    - **Radarr (Movies):** Same deal as Sonarr, but for movies – pulling metadata, file sizes, paths, and enabling automated movie management.
- **Scanning & Analysis:**
    - The app scans your libraries, identifying all your movies and TV shows.
    - It then **cross-references this with Emby playback data** to pinpoint what’s truly unwatched within a **configurable time period** (like "unwatched for 365 days").
    - And get this: It has **intelligent filtering**! It smartly ignores recently added content (e.g., "added within 270 days") so you actually have time to watch your new media.
- **Actionable Insights:**
    - Ultimately, you get a **comprehensive list of unwatched media**.
    - You can filter by media type (movies vs. TV shows) and, crucially, **sort by storage size** to find those space-hogging unwatched items.
    - It displays detailed metadata like date added, file sizes, and even the root folders.
    - All this info helps you make **informed decisions** about what to keep or what to finally kick to the curb.

#### The Engine Under the Hood: Technical Architecture Deep Dive

I built this beast as a **monorepo**, which just makes separating and managing the components so much cleaner.

- **Backend (FastAPI):**
    - **Purpose:** This is the brain, handling all the core logic and providing the **REST APIs** for data collection and processing.
    - **Tech Stack:** Built with the **FastAPI web framework**, using **SQLite** for persistent storage of scan results (simple, but effective for now). It leverages **async/await patterns** throughout for efficient concurrent processing, and I’m using Poetry for dependency management.
- **Frontend (React/TypeScript):**
    - **Purpose:** This is what you actually see – a **responsive, modern web interface** for viewing and interacting with all that juicy data.
    - **Tech Stack:** It's a modern **React application** using **TanStack Router** for smooth navigation, **TypeScript** for solid type safety (prevents so many headaches!), and **Tailwind CSS** for styling, with a slick dark theme. **TanStack Query** handles efficient data fetching and caching.

**Key Technical Highlights:**

- **Type Safety:** Full TypeScript support on the frontend.
- **Modern Async:** The backend is all **async/await** for optimal performance – no waiting around for things to load.
- **Real-time Updates:** It even has **WebSocket-style progress tracking** during scans, so you know exactly what’s happening.
- **Responsive Design:** Works on all devices, mobile-friendly and all that jazz.
- **Configuration Management:** You can configure everything via environment variables, JSON files, or even a web-based settings interface for API keys.

#### Performance Matters: The "Crazy Optimization" Journey

Optimizing this code was a significant challenge, let me tell you. There was this initial "false alarm," and then **Cursor just blew my mind** when I asked it to optimize my code for "Least Watched". What started as a messy approach turned into something way more efficient.

Here are the **key improvements** I implemented:

- **Batch Processing:** Instead of making individual API calls for every single media item, the code now processes media in **batches**. This drastically cuts down the number of API calls, especially to the playback reporting service, which was a huge bottleneck.
- **Playback Data Caching:** I set up a `PlaybackCache` class that stores playback data in memory. This means no more redundant API calls for the same title, which is super handy if you have multiple episodes of the same show or sequels.
- **Efficient Batch Queries:** The `batch_get_playbacks` function now fetches data for multiple titles in a single API call using a combined OR operator. Dramatically reduces network requests.
- **Configurable Batch Size:** Added a `BATCH_SIZE` environment variable, so you can tune the performance based on your specific setup and API limits.
- **Improved Error Handling:** Batch operations are now more robust with fallbacks to individual queries if a batch query fails.
- **Enhanced Performance Metrics:** The code tracks and reports things like cache hit/miss statistics, total execution time, and more detailed progress info. This helps me understand where the time is actually being spent.

The benefits of these optimizations? **Reduced API calls, improved parallelism, better resource utilization, enhanced scalability** for larger media libraries, and just invaluable performance insights.

#### What's Next: Challenges & Future Enhancements

No project is ever truly "done," and "Least Watched" is no different.

- **API Integration Improvements:** The Emby API for getting show and movie information can be a pain ("sucks"). A future goal is to **leverage Sonarr and Radarr APIs more directly** for this.
- **User Experience & Deployment:**
    - I want to implement an **onboarding or setup wizard** – nobody likes a complex first run.
    - Ensuring **smooth database migrations** is crucial, and adding a **backup utility** would be cool.
    - **Dockerizing** the application for easier deployment is high on the list.
    - Setting up **cron jobs** for scheduled scans, so it runs automatically.
    - Adding **user authentication** (user pass, default, and reset password) for better security.
    - Improving **logging** for better debugging and monitoring.
    - And of course, adding **tests** to ensure reliability.
- **Proactive Alerts:** Need to develop **better alerts** for when storage space is running low, so I don't have another Nextcloud meltdown.

#### Final Thoughts

"Least Watched" is my personal effort to bring some order to the ever-growing chaos of a large media collection. It's truly satisfying to have this tool working to free up valuable storage and make content discovery easier. It transforms the tedious task of media management into a seamless, automated process, letting me optimize my storage and curate my libraries effectively.

This project, like my homelab itself, is a constantly evolving beast built from necessity and open-source love. If you're a media enthusiast, a data hoarder, or just someone looking to reclaim some disk space, this is for you.

---