---
author: Sean
pubDatetime: 2025-06-04T19:43:00Z
slug: building-baller-picks
title: "Building Baller Picks: An NBA Pick'em App"
description: An in-depth look at creating a full-stack NBA pick'em PWA using cutting-edge web technologies
featured: false
draft: false
tags:
  - astro
  - docker
  - pocketbase
  - nba
  - typescript
  - project
---

![[../assets/image_baller-picks-banner.png]]

> _An in-depth look at the process and technology behind creating a full-stack NBA pick'em Progressive Web App._

## Table of Contents

## Introduction

I built this project with a simple goal in mind: to create a fun way for my friends and me to engage with NBA games. I've always enjoyed the friendly competition of predicting outcomes, but I'm not a fan of the high-stakes nature of most gambling apps. I wanted a space focused purely on the love of the game.

The result is **Baller Picks**, a sophisticated prediction platform that combines the modern web development ecosystem with real-time sports data. In this post, I'll explore the architecture, technology choices, and implementation details that brought the project to life.

Baller Picks is a comprehensive platform that allows NBA fans (my friends and I) to:

- Predict game outcomes with detailed reasoning and commentary.
- Track performance through statistics and leaderboards.
- Engage with other users' predictions.
- Stay updated with real-time NBA game data and scores.
- Experience fast, native-like performance through PWA capabilities.

The platform leverages real NBA data, providing users with up-to-date matchup information and team statistics to make informed predictions.

![[../assets/image_w-picks-homepage-mobile.png]]

## Technology Choices

Choosing the right technology is critical for any project's success. My goal was to use modern, productive tools that would ensure a high-quality, performant, and maintainable application.

**Frontend Architecture**

- **Astro:** Chosen for its excellent performance characteristics, especially its server-side rendering and "island architecture" which minimizes client-side JavaScript.
- **React:** Used for building interactive UI elements where complex state management is needed.
- **TailwindCSS:** A utility-first CSS framework that speeds up the styling process immensely.
- **ShadCN/UI & Lucide React:** A component library and icon set that provide beautiful, accessible UI primitives, allowing for rapid development of a polished interface.

**Backend & Database**

- **PocketBase:** An efficient and easy to use backend solution. It handles the database (SQLite), user authentication, and API, which allowed me to focus on the application's core features.
- **Astro Server:** Leveraged for server-side rendering (SSR) and creating API routes within the Astro project itself. This server also handles cron jobs to process picks and scoreboard data.

**Development & Tooling**

- **TypeScript:** Applied throughout the entire application to ensure type safety from the frontend to the backend.
- **Zod:** Used for schema declaration and runtime validation, guaranteeing data integrity.
- **pnpm:** A fast and disk-space-efficient package manager.

**State Management & Data Fetching**

- **Nanostores:** A lightweight, framework-agnostic library for sharing state across UI components.
- **TanStack Query:** Implemented for managing server state, handling caching, and simplifying data fetching logic.

## Architecture Deep Dive

The application's foundation is a well-structured database schema, designed to be both efficient and scalable. I used Zod to define schemas that serve as a single source of truth for data shapes, providing both runtime validation and static TypeScript types.

The schema is centered around three core collections: `Users`, `Matchups`, and `Picks`. The `Picks` collection is the heart of the system, linking a user to a specific matchup along with their prediction.

Here is the Zod schema for a "Pick":

TypeScript

```
// This schema defines the structure for a single prediction
export const PickZ = BaseZ.extend({
  matchup: z.string().length(15),      // The unique ID of the game
  win_prediction: z.string().length(3), // The predicted winning team's code
  comment: z.string(),                  // The user's comment on their pick
  user: z.string().length(15),          // The user who made the pick
  status: z.string(),                   // The result of the pick (e.g., 'WIN', 'LOSS')
  // ...and other relevant fields
});

// This command infers a static TypeScript type from the Zod schema
export type PickType = z.infer<typeof PickZ>;
```

This approach ensures that data conforms to the expected structure throughout the application, from database queries to API responses to frontend components, which significantly reduces runtime errors.

![[../assets/image_baller-picks-db-schema.png]]
_Entity Relationship Diagram_

## Key Feature Implementation

Here is a look at how some of the application's primary features were built.

![[../assets/image_baller-picks-pick-interface.png]]
_matchup interface before the game happens, and no picks are present_
![[../assets/image_baller-picks-list.png]]
_matchup interface after the game has ended and picks are locked_

1. Real-Time NBA Data Integration

To provide timely and accurate information, the platform automatically synchronizes with an external NBA data source. I wrote a series of cron jobs that run on a schedule to fetch game schedules, team records, and live scoreboard updates. A robust tracking and logging system monitors these jobs to ensure data remains fresh and reliable.

2. Progressive Web App (PWA) Capabilities

To provide an experience closer to a native mobile app, Baller Picks was built as a PWA. This includes a service worker for caching strategies and offline access, a web app manifest, and a responsive design optimized for all screen sizes. Users can install the app to their home screen for easy access.

![[../assets/image_baller-picks-pwa-install.png]]

3. User Statistics & Performance Tracking

A key feature is the ability for users to track their prediction performance. I developed a system that calculates weekly and overall statistics, such as win/loss ratios and correct pick percentages. These stats are displayed on user profiles and aggregated into a site-wide leaderboard.

![[../assets/image_baller-picks-user-stats.png]]
_user stats on profile page_

## Key Takeaways

This project was a valuable learning experience. These were some of my most important takeaways:

1. **End-to-End Type Safety is a Worthwhile Investment:** Using Zod and TypeScript across the entire stack created a more resilient application and saved significant debugging time.
2. **Server-Side Rendering Delivers a Better UX:** Astro's performance-first approach to SSR results in faster initial page loads and a smoother user experience.
3. **Leveraging a BaaS Can Accelerate Development:** Using PocketBase for the backend abstracted away much of the complexity of database and auth management, allowing me to focus on frontend and feature development.
4. **A Good User Experience is Multifaceted:** It's the combination of a clean UI, fast performance (SSR), and useful features (PWA capabilities) that creates a truly engaging product.

## Conclusion

Baller Picks demonstrates a comprehensive approach to building modern web applications. By combining Astro's server-side rendering with a type-safe backend, the platform delivers strong performance while maintaining developer productivity. It successfully fulfills my initial goal of creating an engaging, data-driven sports application that prioritizes community fun over gambling.

The project showcases how thoughtful technology choices can lead to applications that are both powerful for developers and delightful for users.

---

_For those interested in exploring the implementation further, the project's codebase demonstrates advanced patterns in Astro, TypeScript integration, and real-time data management. Check it out on my GitHub [here](https://github.com/seansusmilch/w-picks-astro)_
