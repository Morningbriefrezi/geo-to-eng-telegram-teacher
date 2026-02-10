#!/usr/bin/env python3
"""
Geo → Eng Daily Telegram Teacher
Two modes:
  - words   (30 words)   morning
  - grammar (micro lesson) evening

This script is designed to be run by GitHub Actions on a schedule (free).
It reads secrets from environment variables (GitHub repo Secrets):
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID
Optional:
  START_DATE (YYYY-MM-DD)  # day 1 of the 14-day plan; default = today in Tbilisi
  CURRICULUM_PATH          # default = curriculum.json
  MODE                      # words | grammar
"""

import os
import json
import sys
import datetime as dt
import urllib.parse
import urllib.request

TBILISI_OFFSET_HOURS = 4  # Georgia is UTC+4 (no DST)

def tbilisi_today() -> dt.date:
    now_utc = dt.datetime.utcnow()
    now_tbilisi = now_utc + dt.timedelta(hours=TBILISI_OFFSET_HOURS)
    return now_tbilisi.date()

def load_curriculum(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_day_index(start_date: str | None, total_days: int) -> int:
    if start_date:
        s = dt.date.fromisoformat(start_date)
    else:
        s = tbilisi_today()
    today = tbilisi_today()
    delta = (today - s).days
    # loop 1..total_days
    return (delta % total_days)

def format_words(day_obj) -> str:
    theme = f"📚 Day {day_obj['day']} — {day_obj['theme_en']} / {day_obj['theme_ka']}"
    lines = [theme, "", "🟦 30 New Words (EN — KA):", ""]
    for i, (en, ka) in enumerate(day_obj["words"], start=1):
        lines.append(f"{i:02d}. {en} — {ka}")
    lines.append("")
    lines.append("✅ Mini task / მცირე დავალება:")
    lines.append("Pick 5 words and write 1 sentence for each (EN).")
    lines.append("აირჩიე 5 სიტყვა და თითოეულზე დაწერე 1 წინადადება (ინგლისურად).")
    return "\n".join(lines)

def format_grammar(day_obj) -> str:
    g = day_obj["grammar"]
    theme = f"🧠 Day {day_obj['day']} — Grammar / გრამატიკა"
    lines = [theme, "", f"🔸 {g['title_en']}", f"🔹 {g['title_ka']}", ""]
    lines += ["EN:", g["explanation_en"], "", "KA:", g["explanation_ka"], ""]
    lines.append("Examples / მაგალითები:")
    for ex in g["examples"]:
        lines.append(f"• {ex['en']}")
        lines.append(f"  — {ex['ka']}")
    lines.append("")
    lines.append("Mini quiz / მცირე ტესტი:")
    for q in g["mini_quiz"]:
        lines.append(f"Q: {q['q_en']}")
        lines.append(f"კითხვა: {q['q_ka']}")
        lines.append(f"✅ Answer: {q['a_en']}")
        lines.append("")
    lines.append("🔥 Challenge / ჩელენჯი:")
    lines.append("Reply to yourself with 2 original sentences using today’s grammar.")
    lines.append("დაწერე 2 საკუთარი წინადადება დღევანდელი გრამატიკით.")
    return "\n".join(lines).strip()

def send_telegram_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
        if resp.status != 200:
            raise RuntimeError(f"Telegram API error: {resp.status} {body}")

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID", file=sys.stderr)
        sys.exit(1)

    mode = os.getenv("MODE", "words").strip().lower()
    curriculum_path = os.getenv("CURRICULUM_PATH", "curriculum.json").strip()
    start_date = os.getenv("START_DATE", "").strip() or None

    curriculum = load_curriculum(curriculum_path)
    idx = get_day_index(start_date, total_days=len(curriculum))
    day_obj = curriculum[idx]

    if mode == "grammar":
        msg = format_grammar(day_obj)
    else:
        msg = format_words(day_obj)

    signature = "\n\nსიყვარულით რეზისგან 🥰"
send_telegram_message(token, chat_id, msg + signature)

    print("Sent:", mode, "Day", day_obj["day"])

if __name__ == "__main__":
    main()
