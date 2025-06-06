---
author: Sean
pubDatetime: 2024-10-02T05:35:45.644Z
slug: creating-a-reverse-split-arbitrage-newsletter
title: Creating a Reverse Split Arbitrage Newsletter
description: How I created a newsletter that scrapes for profitable reverse split opportunities using python.
featured: true
draft: false
tags:
  - python
  - stocks
  - investing
  - ai
  - llm
  - web-scraping
  - project
  - pocketbase
---
Here's a writeup of my experience creating a newsletter that gives profitable reverse split opportunities. **I YAP A LOT** so don't hesitate to skip around with the TOC.

>Disclaimer: Please remember that any investment involves risk, and that this newsletter is not to be used as financial advice. Do your own research before coming to any sort of financial decisions.

## Update June 2025!!!
Lately, my reverse splits have not been going through on Robinhood. They've been getting sold instead of rounded up despite the announcements saying they would do so. I have not investigated this too much. 

However Kenny Peng, the one behind revRSS, detailed in a post [here](https://www.revrss.com/2025/05/04/manipulation_investigations_2.html) and [here](https://www.revrss.com/2024/11/02/manipulation_investigations.html) his research into the matter. His posts detail a company's litigations based on accusations of stock manipulation due to the sharp rise in shareholders shortly before their split. I won't go into detail in this update, so I highly suggest reading Kenny's posts if you're interested. Personally, I do not believe this is stock manipulation as people are just reacting to publicly available news... but I'm not very informed on the matter.

Either way, as Kenny said in his post, this has become a legal grey area and I don't want to be caught up in it. Especially if Robinhood (or someone else along the chain) no longer delivers on rounded splits.

**Due to these developments, I have stopped this service on June 5th, 2025**


## Table of contents

## Inspiration

Yes, I'm in that hustle mindset. I really enjoy stocks and other sorts of investing. Also, I've always wanted to create some sort of newsletter, but I couldn't pin down what value I wanted to bring to my 0 million subscribers. The creation of this newsletter would prove to be (in my opinion) a good meshing of my skills as a software engineer and my interests in investing.

### First Exposure to Reverse Splits

I first came across the reverse split arbitrage strategy in a friend's Discord server. No, not one of those scammy one's; it was a server for the friend group. Basically, one of my friend's friends would just post in a dedicated channel that "this stock is doing a reverse split! Buy 1 share before this date!".

At first I didn't think much of it. What's a "reverse split"? What the hell are they talking about?

![confused emoji](https://media.tenor.com/4_41a1_Ha_UAAAAi/i%27m-confused.gif)
*Me af*

### The Reverse Split Arbitrage Strategy

For those who don't know, the reverse split arbitrage strategy is a stock trading strategy that works by taking advantage of companies that round up fractional shares when they are performing a stock share consolidation. I won't get in too deep here, but Kenny Peng has a fantastic writeup of the strategy in the first few paragraphs on the [revRSS](https://www.revrss.com/) homepage. I've taken many pointers from his revRSS project and I have used the product for some time before making this.

Essentially, this strategy takes a few steps to pull off:

1. Finding a company that is performing a reverse split
2. Knowing if the company will be **rounding up fractional shares**
3. You must buy 1 share prior to the effective date of the reverse split

The main sources of friction in this strategy are the first 2 steps. Searching which companies are performing reverse splits, and then sifting and skimming through press releases to determine if they're rounding up fractional shares. All that effort makes it less and less worth the measly payout.

Unless???

## Value Added

I created this newsletter with the goal of making it dead simple to know when companies are performing reverse splits, and if they're rounding up fractional shares. I've put some time into getting accurate split calendars, full press release articles, and even an AI generated summary that will let you know whether the press release mentions rounding up fractional shares! This achieves my goal in reducing friction of executing this strategy by a decent amount. However, there are still many things that could be improved.
## The Architecture

Here's a rundown of the architecture and design choices I made when creating this project. The architecture of this project is fairly simple in the sense that a good portion of it is abstracted away for me. I separated the project into 4 main components.
![reverse-splitter-stack.png](@/assets/blog/reverse-splitter-stack.png)
*The tech stack*

### Emails (Brevo)

With a newsletter, and email in general, there are many factors that can impact your email deliverability, government compliance, etc. I did not want to think of all that... I wanted to ship, so I chose Brevo as my email provider. I already had an account set up, and they also have a very generous free tier. The main role of Brevo in this project is as follows:

* Handle email contacts (subscribers/unsubscribes)
* Handle sending all newsletters/campaigns

### Database (Pocketbase)

I want to focus on other parts of the project, not learning a new database. For that reason, I chose Pocketbase as my database. It's just so nice in terms of a decent feature set and API docs. While there's no official library for Python, there are good unofficial libraries that do everything I need. The database will handle the following:

* New email subscriptions (not yet in Brevo)
* Upcoming reverse splits
* Keep track of whether a reverse split was already sent in a newsletter

### Subscribe Form (AstroJS)

This is pretty much just a simple form that will collect a user's name and email when they want to be subscribed to the newsletter. I chose Astro because I feel it's very quick to set something like this up, plus it gives support for top-level await which I like.

* Submit new subscribers to the backend
* Give users a quick rundown on reverse splits and how to profit off them

### Backend (Python)

I chose Python because it's familiar to me and fast (to write!!!) I suppose this can be further split up... but the main jobs of the backend is as follows:

* Add new subscribers to Brevo
* Scrape for upcoming reverse splits
* Scrape for press releases regarding reverse splits
* Summarize press releases
* Generate newsletter html and send with Brevo

## Limitations/Challenges

This project faced a multitude of challenges. One of the biggest, was definitely finding a calendar that laid out upcoming reverse splits in an easily scrapable way. Many calendars were behind authentication, or other odd blockers that made it a pain to scrape. 

The accuracy of such calendars was also something I questioned a bit. It always felt like I was missing out on opportunities

Interested in checking out the code? Find it [here](https://seansusmilch.github.io/posts/creating-a-reverse-split-arbitrage-newsletter/) on my GitHub!