from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.jackpot import spin_jackpot

app = FastAPI(title="Jackpot Game Web")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/spin")
def spin():
    result, jackpot = spin_jackpot()

    return {
        "slots": result,
        "jackpot": jackpot
    }