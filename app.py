import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
CATEGORIES = ["Food", "Travel", "Books", "Entertainment", "Bills", "Other"]


def get_db():
    conn = sqlite3.connect(os.environ.get("DB_PATH", "expenses.db"))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS expenses(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               amount REAL NOT NULL,
               category TEXT NOT NULL,
               date TEXT NOT NULL)"""
        )


@app.route("/")
def index():
    cat = request.args.get("category", "")
    with get_db() as c:
        if cat:
            rows = c.execute("SELECT * FROM expenses WHERE category=? ORDER BY date DESC, id DESC", (cat,)).fetchall()
        else:
            rows = c.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC").fetchall()
        totals = c.execute("SELECT category, SUM(amount) AS total FROM expenses GROUP BY category").fetchall()
    grand = sum(r["total"] for r in totals)
    return render_template("index.html", expenses=rows, totals=totals, grand=grand,
                           categories=CATEGORIES, selected=cat, today=date.today().isoformat())


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"].strip()
    try:
        amount = float(request.form["amount"])
    except ValueError:
        return "Invalid amount", 400
    if not title or amount <= 0:
        return "Title required and amount must be positive", 400
    with get_db() as c:
        c.execute("INSERT INTO expenses(title,amount,category,date) VALUES(?,?,?,?)",
                  (title, amount, request.form["category"], request.form["date"]))
    return redirect(url_for("index"))


@app.route("/edit/<int:eid>", methods=["GET", "POST"])
def edit(eid):
    with get_db() as c:
        if request.method == "POST":
            c.execute("UPDATE expenses SET title=?, amount=?, category=?, date=? WHERE id=?",
                      (request.form["title"].strip(), float(request.form["amount"]),
                       request.form["category"], request.form["date"], eid))
            return redirect(url_for("index"))
        row = c.execute("SELECT * FROM expenses WHERE id=?", (eid,)).fetchone()
    if row is None:
        return "Not found", 404
    return render_template("edit.html", e=row, categories=CATEGORIES)


@app.route("/delete/<int:eid>", methods=["POST"])
def delete(eid):
    with get_db() as c:
        c.execute("DELETE FROM expenses WHERE id=?", (eid,))
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
