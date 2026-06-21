import random
import logging

logger = logging.getLogger(__name__)

symbols = ["🍒", "🍋", "⭐", "💎", "7️⃣"]


def spin_jackpot():
    logger.info("spin_jackpot 함수 시작")

    result = [
        random.choice(symbols),
        random.choice(symbols),
        random.choice(symbols)
    ]

    jackpot = result[0] == result[1] == result[2]

    if jackpot:
        logger.info(f"JACKPOT 성공: result={result}")
    else:
        logger.info(f"JACKPOT 실패: result={result}")

    return result, jackpot