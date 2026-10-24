# Smart Expense Tracker — Experiment 10 Mini Project

A web app for students to record, edit, filter and summarise daily expenses.
**Stack:** Python, Flask, SQLite, HTML/CSS · **Tools:** Git, JIRA, Docker, localhost deployment.

## Features
Add / edit / delete expenses · category filter · category-wise totals · health endpoint · unit tests

## Run locally (without Docker)
```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # http://localhost:5000
pytest                           # run tests
```

## Run with Docker (deployment on localhost)
```
docker build -t expense-tracker .
docker run -d -p 5000:5000 -v expense_data:/data --name expense-tracker expense-tracker
# or simply:
docker compose up -d --build
```
Open http://localhost:5000 · Stop: `docker compose down`

## Project structure
```
app.py            Flask routes + SQLite logic
templates/        HTML (base, index, edit)
tests/            pytest tests
Dockerfile        container image
docker-compose.yml  one-command deployment
```
