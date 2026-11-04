# Course Module Builder

Admin-only tool that creates new QuizKerala-style apps ("modules"). Each new
module gets its own GitHub repo, database, Vercel project and a subdomain on
`calecutech.com`.

## Status

| Step | State |
|---|---|
| 1. Builder admin page (settings form, tickable features) | Done |
| 2. "Create app": copy QuizKerala into a new repo | Not started |
| 3. Database + Vercel project + subdomain per app | Not started |
| 4. First app: JAIIB exam preparation | Not started |

See [docs/PLAN.md](docs/PLAN.md) for decisions and the roadmap.

## What it does today

- `/admin/login`: sign in with `ADMIN_TOKEN`
- `/admin/apps`: list saved apps and add a new one
- A new app records: name, subdomain, topic, extra AI prompt, payment provider
  (Razorpay or Stripe) and the features to include

Apps are saved to `data/apps.json`. **This works locally only.** On Vercel the
filesystem is read-only, so saving fails until storage moves to a database.

## Run locally

```bash
npm install
ADMIN_TOKEN=choose-a-password npm run dev
```

Open http://localhost:3000 and sign in.

## Environment variables

| Name | Used for |
|---|---|
| `ADMIN_TOKEN` | Admin sign-in password |
| `GITHUB_TOKEN` | Creating repos for new apps (step 2). Needs Administration + Contents write on `vsvivek1`. |

Never commit these. On Vercel they are saved as sensitive variables.

## Deploy

Vercel project `course-module-builder`, built from the `main` branch of this repo.

## Domains

New apps live at `<subdomain>.calecutech.com`. DNS for `calecutech.com` is on
Squarespace, which has no API, so one wildcard record was added by hand:

- Type `CNAME`, Host `*`, Data `cname.vercel-dns.com`

Each app's subdomain is then attached to its Vercel project by the builder.
