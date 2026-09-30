# Chalk & Slate

Two-player tic-tac-toe on a hand-drawn chalkboard. Every X, O, and winning line is animated as a chalk stroke in SVG.

There are two versions:

- **`chalk-and-slate.html`**: a single-file version in HTML, CSS, and JavaScript. The scoreboard (X wins, O wins, draws) is saved in localStorage, so it's still there on your next visit.
- **`webapp/`**: a Flask version where the board, turns, and score live server-side in the session. Every move is a normal form submit, so it plays with no client-side JavaScript at all.

## Run it

**Single-file version:** open `chalk-and-slate.html` in a browser.

**Flask version:**

```bash
cd webapp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5050.

## Tech

HTML, CSS, JavaScript, SVG, Python, Flask
