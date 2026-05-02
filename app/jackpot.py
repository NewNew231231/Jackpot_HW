import random

symbols = ["🍒", "🍋", "⭐", "💎", "7️⃣"]

def spin_jackpot():
    result = [
        random.choice(symbols),
        random.choice(symbols),
        random.choice(symbols)
    ]

    jackpot = result[0] == result[1] == result[2]

    return result, jackpot