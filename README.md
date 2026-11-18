# Chess game review emails

After every chess.com game you finish, you get an email with a link to a full review:
accuracy for both players, every move classified (brilliant, great, best, excellent, good,
book, inaccuracy, mistake, blunder), the engine's best move with an arrow and line, an eval
bar and graph, and a list of key moments.

How it works:
- **GitHub Actions** (free) checks your chess.com account every ~10 minutes and emails you
  through Gmail when a new game shows up.
- **GitHub Pages** (free) hosts `index.html`, the review page. When you open the link,
  Stockfish analyzes the game right in your browser. That takes about 20–40 seconds the first
  time and is instant after that.

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
- **Timing:** GitHub's scheduler can run late, sometimes by 15+ minutes when it's busy.
- **Depth:** reviews default to depth 14. Use the depth dropdown on the page for a deeper,
  slower analysis.
- **Accuracy and labels:** this uses the open, Lichess-style accuracy formula and its own
  move-classification rules. Numbers will be close to chess.com's Game Review but not
  identical. "Brilliant" and "Book" are heuristics.
- **Variants** (Chess960, etc.) are skipped. Only standard chess is reviewed.
- **Inactivity:** GitHub pauses scheduled workflows after 60 days with no repository activity.
  If emails stop, open the Actions tab and re-enable the workflow.
- **Troubleshooting:** in the Actions tab, click a run to see its log. A Gmail login error
  means the app password or `GMAIL_ADDRESS` secret is wrong.
