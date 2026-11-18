"""Checks chess.com for newly finished games and emails a review link for each one.

Runs inside GitHub Actions (see .github/workflows/chess-review.yml). Uses only the
Python standard library. Settings come from environment variables / repo secrets:

  CHESS_USERNAME      your chess.com username
  GMAIL_ADDRESS       the Gmail account that sends the email
  GMAIL_APP_PASSWORD  a Gmail "app password" (not your normal password)
  TO_EMAIL            optional, where to send (defaults to GMAIL_ADDRESS)
  SITE_URL            optional, where index.html is hosted (defaults to GitHub Pages URL)
"""
import html
import json
import os
import smtplib
import time
import urllib.request
from email.message import EmailMessage
from pathlib import Path

STATE_FILE = Path(__file__).with_name("state.json")
USER = os.environ["CHESS_USERNAME"].strip().lower()
SENDER = os.environ["GMAIL_ADDRESS"].strip()
PASSWORD = os.environ["GMAIL_APP_PASSWORD"].replace(" ", "")
TO = (os.environ.get("TO_EMAIL") or "").strip() or SENDER


def site_url():
    if os.environ.get("SITE_URL"):
        return os.environ["SITE_URL"].rstrip("/")
    owner, repo = os.environ["GITHUB_REPOSITORY"].split("/")
    if repo.lower() == f"{owner.lower()}.github.io":
        return f"https://{owner.lower()}.github.io"
    return f"https://{owner.lower()}.github.io/{repo}"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "personal-game-review-notifier/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


DRAWS = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}
HOW = {"checkmated": "checkmate", "resigned": "resignation", "timeout": "time", "abandoned": "abandonment"}


def describe(game):
    white, black = game["white"], game["black"]
    me, opp = (white, black) if white["username"].lower() == USER else (black, white)
    if me["result"] == "win":
        outcome = f"Won by {HOW.get(opp['result'], opp['result'])}"
    elif me["result"] in DRAWS:
        outcome = f"Draw ({me['result']})"
    else:
        outcome = f"Lost by {HOW.get(me['result'], me['result'])}"
    return me, opp, outcome


def send_email(game, month, site):
    me, opp, outcome = describe(game)
    game_id = game["url"].rstrip("/").split("/")[-1]
    link = f"{site}/?user={USER}&id={game_id}&month={month}"
    subject = f"Game review: vs {opp['username']} ({opp['rating']}) - {outcome}"
    text = f"{outcome} vs {opp['username']} ({opp['rating']}), {game.get('time_class', '')}.\n\nReview: {link}\nGame on chess.com: {game['url']}\n"
    body = f"""<div style="font-family:Segoe UI,Arial,sans-serif;max-width:520px">
      <h2 style="margin:0 0 6px">{html.escape(outcome)}</h2>
      <p style="margin:0 0 16px;color:#555">You ({me['rating']}) vs <b>{html.escape(opp['username'])}</b> ({opp['rating']}) &middot; {html.escape(game.get('time_class', ''))}</p>
      <a href="{link}" style="display:inline-block;background:#2563eb;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:600">Open game review</a>
      <p style="margin-top:16px;font-size:13px;color:#777">Accuracy, move-by-move classifications, best moves and the eval graph.
      <br><a href="{game['url']}">View the game on chess.com</a></p></div>"""

    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, SENDER, TO
    msg.set_content(text)
    msg.add_alternative(body, subtype="html")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
        s.login(SENDER, PASSWORD)
        s.send_message(msg)
    print(f"Emailed review for {game['url']}")


def main():
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    last = state.get("last_end_time", 0)

    if not last:
        # First run: start from now so you don't get emailed your whole history.
        state["last_end_time"] = int(time.time())
        STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
        print("First run: will email reviews for games finished from now on.")
        return

    archives = get(f"https://api.chess.com/pub/player/{USER}/games/archives")["archives"][-2:]
    new = []
    for url in archives:
        month = url.split("/games/")[1]
        for g in get(url).get("games", []):
            if g.get("end_time", 0) > last and g.get("rules") == "chess":
                new.append((g, month))
    new.sort(key=lambda x: x[0]["end_time"])

    site = site_url()
    for game, month in new[-10:]:  # never send more than 10 at once
        send_email(game, month, site)
        state["last_end_time"] = game["end_time"]
        STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    if new and len(new) > 10:
        state["last_end_time"] = new[-1][0]["end_time"]
        STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    print(f"{len(new)} new game(s).")


if __name__ == "__main__":
    main()
