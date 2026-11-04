# Plan and decisions

## Goal

One admin-only module that can generate another module with the features of
QuizKerala, each with its own repo and admin panel.

## Decisions (from vivek)

- Domain: `calecutech.com`, apps at `name.calecutech.com`
- DNS: Squarespace, one manual wildcard CNAME (see README)
- Creation: from an admin page in this builder, template plus an extra AI prompt
- Each app: own GitHub repo, own database, own Vercel project
- Social accounts (YouTube, Facebook, Instagram): tokens and IDs entered per app
- Payments: Razorpay or Stripe, chosen per app
- First app: JAIIB exam preparation
- GitHub repos are created with a `GITHUB_TOKEN` stored in Vercel

## Features a new app can include

Tick any of these when creating an app:

- Timed quizzes, leaderboard, results
- Question banks and file import
- AI question generator
- Fact generator
- 365-day content schedule
- Publish to YouTube, Instagram, Facebook
- Affiliate product links
- Invite and result emails
- Paid courses and quiz series (Pro)
- Android app (Play Store build)

Exam-specific pages in QuizKerala (PSC, US citizenship, USS) are not offered.

## Roadmap

1. Builder admin page. **Done.**
2. Move app settings from `data/apps.json` to a database (needed on Vercel).
3. "Create app": create the GitHub repo and copy the QuizKerala template with
   only the ticked features, plus the extra prompt.
4. Create the database and Vercel project, attach the subdomain, set env vars.
5. Generate JAIIB prep as the first real app and check its admin, AI
   question and fact generators, schedule and social posting.

## Known limits

- Saving apps fails on Vercel until step 2 is done.
- Admin sign-in is one shared token, not per-user accounts.
- Social tokens are not stored yet; they need encryption before they are.
