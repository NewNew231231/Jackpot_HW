import logging
import traceback

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.jackpot import spin_jackpot
from app.issue import create_github_issue


# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("jackpot.log", encoding="utf-8")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


app = FastAPI(title="Jackpot Game Web")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    logger.info("GET / 요청 - 메인 페이지 접속")

    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/spin")
def spin():
    try:
        logger.info("GET /spin 요청 - 잭팟 게임 실행")

        result, jackpot = spin_jackpot()

        logger.info(f"SUCCESS /spin | result={result}, jackpot={jackpot}")

        return {
            "slots": result,
            "jackpot": jackpot
        }

    except Exception as e:
        logger.exception(
            f"FAIL /spin | error={type(e).__name__}: {e}"
        )

        tb = traceback.format_exc()

        title = f"[Prod Error] /spin failed: {type(e).__name__}"

        body = (
            f"## Summary\n"
            f"- endpoint: /spin\n"
            f"- project: jackpot-game\n\n"
            f"## Exception\n"
            f"- type: {type(e).__name__}\n"
            f"- message: {str(e)}\n\n"
            f"## Traceback\n"
            f"```text\n{tb}\n```"
        )

        create_github_issue(title, body, logger)

        return {
            "message": "Internal Server Error",
            "slots": [],
            "jackpot": False
        }