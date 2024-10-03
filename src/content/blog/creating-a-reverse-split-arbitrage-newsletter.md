---
author: Sean
pubDatetime: 2024-10-02T05:35:45.644Z
slug: creating-a-reverse-split-arbitrage-newsletter
title: Creating a Reverse Split Arbitrage Newsletter
description: How I created a newsletter that scrapes for profitable reverse split opportunities using python.
featured: true
tags:
- python
- stocks
- investing
- ai
- llm
draft: false
---

Here's a writeup of my experience creating a newsletter that gives profitable reverse split opportunities.

Disclaimer: Please remember that any investment involves risk, and that this newsletter is not to be used as financial advice. Do your own research before coming to any sort of financial decisions.

## Table of contents

## Inspiration

Yes, I'm in that hustle mindset. I really enjoy stocks and other sorts of investing. Also, I've always wanted to create some sort of newsletter, but I couldn't pin down what value I wanted to bring to my 0 million subscribers. The creation of this newsletter would prove to be (in my opinion) a good meshing of my skills as a software engineer and my interests in investing.

### First Exposure to Reverse Splits

I first came across the reverse split arbitrage strategy in a friend-of-mine's discord server. No, not one of those scammy one's, it was a server for the friend group. Basically, one of my friend's friends would just post in a dedicated channel that "this stock is doing a reverse split! Buy 1 share before this date!".

At first I didn't think much of it. What's a "reverse split"? What the hell are they talking about?

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

