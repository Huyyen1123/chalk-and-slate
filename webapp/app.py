"""Chalk & Slate — a chalkboard tic-tac-toe, served by Flask.

Game state (board, whose turn, running score) lives server-side in the
session; every move is a real page load, no client-side JS required.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5050
"""

import os

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("CHALK_SLATE_SECRET", "dev-secret-change-me")

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


def new_state():
    return {
        "board": [None] * 9,
        "current": "X",
        "over": False,
        "winner": None,       # 'X' | 'O' | None (None + over=True means a draw)
        "win_line": None,     # (a, b, c) indices, once someone has won
        "scores": {"X": 0, "O": 0, "D": 0},
    }


def get_state():
    if "state" not in session:
        session["state"] = new_state()
    return session["state"]


def save_state(state):
    session["state"] = state  # reassignment marks the session modified


def cell_center(i):
    col, row = i % 3, i // 3
    return 50 + col * 100, 50 + row * 100


def check_win(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return (a, b, c)
    return None


def build_context(state):
    win_line = None
    if state["win_line"]:
        a, c = state["win_line"][0], state["win_line"][2]
        x1, y1 = cell_center(a)
        x2, y2 = cell_center(c)
        win_line = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    return {
        "board": state["board"],
        "current": state["current"],
        "game_over": state["over"],
        "winner": state["winner"],
        "win_line": win_line,
        "scores": state["scores"],
    }


@app.route("/")
def index():
    return render_template("index.html", **build_context(get_state()))


@app.route("/move", methods=["POST"])
def move():
    state = get_state()
    if not state["over"]:
        try:
            i = int(request.form["i"])
        except (KeyError, ValueError):
            i = -1
        if 0 <= i < 9 and state["board"][i] is None:
            player = state["current"]
            state["board"][i] = player

            line = check_win(state["board"])
            if line:
                state["over"] = True
                state["winner"] = player
                state["win_line"] = line
                state["scores"][player] += 1
            elif all(state["board"]):
                state["over"] = True
                state["scores"]["D"] += 1
            else:
                state["current"] = "O" if player == "X" else "X"
    save_state(state)
    return redirect(url_for("index"))


@app.route("/new", methods=["POST"])
def new_game():
    scores = get_state()["scores"]
    state = new_state()
    state["scores"] = scores
    save_state(state)
    return redirect(url_for("index"))


@app.route("/reset-score", methods=["POST"])
def reset_score():
    state = get_state()
    state["scores"] = {"X": 0, "O": 0, "D": 0}
    save_state(state)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
