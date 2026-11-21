# Chess game review emails

After every chess.com game you finish, you get an email with a link to a full review:
accuracy for both players, every move classified (brilliant, great, best, excellent, good,
book, inaccuracy, mistake, blunder), the engine's best move with an arrow and line, an eval
bar and graph, and a list of key moments. Every move also gets a short plain-English
explanation of what it does, or why it loses ground and what the better move was.

How it works:
- **GitHub Actions** (free) checks your chess.com account every ~10 minutes and emails you
  through Gmail when a new game shows up.
- **GitHub Pages** (free) hosts `index.html`, the review page. When you open the link,
  Stockfish analyzes the game right in your browser. That takes about 20–40 seconds the first
  time (less on a fast computer), and you can start stepping through the moves right away.
  Reopening it later is instant.

Nothing has to run on your own computer.

---

## Setup (about 15 minutes, all in the browser)

### 1. Get a Gmail app password
1. Turn on 2-Step Verification for your Google account (required for app passwords).
2. Go to https://myaccount.google.com/apppasswords, create one named "chess review",
   and copy the 16-character password.

### 2. Create the GitHub repository
1. Sign up at https://github.com if you don't have an account.
2. Click **New repository**, name it e.g. `chess-review`, set it to **Public** (free Pages
   needs that; your password stays hidden in Secrets), and create it.
3. Click **uploading an existing file** and drag in `index.html`, `notify.py` and `README.md`.
   Commit.
4. Click **Add file → Create new file**. Name it exactly
   `.github/workflows/chess-review.yml`, paste in the contents of that file from this
   folder, and commit.

### 3. Add your secrets
Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

| Name | Value |
|---|---|
| `GMAIL_ADDRESS` | your Gmail address (it sends the email to itself) |
| `GMAIL_APP_PASSWORD` | the 16-character app password from step 1 |

The chess.com username is already filled in inside `.github/workflows/chess-review.yml`.

### 4. Turn on GitHub Pages
**Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main`,
folder `/ (root)` → Save.** After a minute your page is live at
`https://YOUR-GITHUB-NAME.github.io/chess-review/`.

Test it: open `https://YOUR-GITHUB-NAME.github.io/chess-review/?user=YOUR-CHESS-USERNAME`
and click any game.

### 5. Start the checker
Open the **Actions** tab, click **Email game reviews → Run workflow**. The first run only records
"now" as the starting point, so you don't get emails for your old games. After that it runs
by itself every ~10 minutes.

Play a game, and the review email arrives within about 10–20 minutes.

---

## Good to know
- **Timing:** the checker is scheduled every 10 minutes, but GitHub's scheduler is
  best-effort. Runs are often delayed, sometimes by 15–30+ minutes when GitHub is busy, and
  occasionally skipped. A late email is normal and doesn't mean anything is broken. You can
  always run it by hand from the Actions tab.
- **Move explanations:** while stepping through a game, the coach panel explains each move in
  1–3 sentences: what it does (develops, captures, forks, gives check, defends a loose piece),
  and for inaccuracies, mistakes and blunders, what it allowed and what the better move was
  (for example, that it wins a piece or forces mate), with the engine line. Great, brilliant
  and bad moves also get a short note right in the move list, so you can read the story of
  the game without tapping anything. The explanations are generated from Stockfish's lines
  and simple board checks, so treat them as a guide. At low depth the engine can misjudge
  sharp positions.
- **Depth:** reviews default to depth 14 on a computer and depth 12 on phones and other
  touch screens, so they finish faster. Use the depth dropdown on the page for a deeper,
  slower analysis.
- **Progressive results:** the board and move list show up right away. Classifications and
  explanations fill in as each position is analyzed, starting with the position you're
  looking at. Progress is saved in your browser, so reopening a review is instant.
- **Accuracy and labels:** this uses the open, Lichess-style accuracy formula and its own
  move-classification rules. Numbers will be close to chess.com's Game Review but not
  identical. "Brilliant" and "Book" are heuristics.
- **Variants** (Chess960, etc.) are skipped. Only standard chess is reviewed.
- **Inactivity:** GitHub pauses scheduled workflows after 60 days with no repository activity.
  If emails stop, open the Actions tab and re-enable the workflow.
- **Troubleshooting:** in the Actions tab, click a run to see its log. A Gmail login error
  means the app password or `GMAIL_ADDRESS` secret is wrong.
