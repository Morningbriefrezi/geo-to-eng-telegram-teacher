# Geo → Eng Daily Telegram Teacher (14 days, B1 → B2)

This repo sends you **two proactive Telegram messages every day** (Tbilisi time):
- **11:00** — *30 new words* (EN + KA)
- **17:00** — *short grammar lesson* (EN + KA)

It runs for **free** using **GitHub Actions** (no server needed).

---

## 1) Create your Telegram bot + get IDs

### A) Create bot token
1. Open Telegram and message **@BotFather**
2. Send: `/newbot`
3. Choose a name + username
4. Copy the **BOT TOKEN** (looks like `123456:ABC...`)

### B) Get your CHAT ID (your own Telegram id or a group id)
**Option 1 (easy):** use @userinfobot  
1. Open Telegram → message **@userinfobot**
2. It will show your **Id** → copy it (example `123456789`)

**Option 2 (group):**  
1. Add your bot to the group
2. Send a message in the group
3. Temporarily run the script locally once with `MODE=words` (see section 4) and read the error if chat id is wrong; then switch to the correct group chat id (often starts with `-100...`).

---

## 2) Put this code on GitHub

### A) Create a repo
1. Go to GitHub → **New repository**
2. Name it e.g. `geo-to-eng-telegram-teacher`
3. Create it (public or private)

### B) Upload files
Upload these files/folders into the repo root:
- `main.py`
- `curriculum.json`
- `requirements.txt`
- `.github/workflows/teacher.yml`

---

## 3) Add GitHub Secrets (IMPORTANT)

In your repo:
**Settings → Secrets and variables → Actions → New repository secret**

Add:
- `TELEGRAM_BOT_TOKEN` = your BotFather token
- `TELEGRAM_CHAT_ID` = your chat id (numbers)
- `START_DATE` = (optional) `2026-02-11` (or any date you want to be Day 1)

---

## 4) Test it right now (no waiting)

Go to:
**Actions → Daily English Teacher → Run workflow**

Choose:
- `mode = words` (test morning message)
- run again with `mode = grammar` (test evening message)

If the secrets are correct, you’ll instantly receive messages in Telegram.

---

## 5) How scheduling works (Tbilisi time)

GitHub Actions uses **UTC**.
Georgia is **UTC+4**, so:
- 11:00 Tbilisi = **07:00 UTC**
- 17:00 Tbilisi = **13:00 UTC**

The workflow already schedules both.

---

## 6) Customize the plan
Edit `curriculum.json`:
- add new days
- change word lists
- change grammar lessons

The bot automatically loops through days.

---

## Troubleshooting
- **No messages:** check Actions logs (Actions → last run → logs).
- **Chat not found:** your `TELEGRAM_CHAT_ID` is wrong.
- **Bot blocked:** open the bot chat and press **Start**.
