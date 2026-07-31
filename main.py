import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Символы и их стоимость за 3 одинаковых в ряд
SYMBOLS = {
    "🍒": 100,  # Черкешня
    "🍋": 250,  # Лимон
    "💎": 500,  # Кристалл
}

COST_PER_SPIN = 150
INITIAL_BALANCE = 2300


@app.route("/")
def index():
    # При каждом открытии/перезагрузке страницы баланс сбрасывается до 1000
    return render_template("index.html", initial_balance=INITIAL_BALANCE)


@app.route("/spin", methods=["POST"])
def spin():
    data = request.get_json()
    current_balance = data.get("balance", INITIAL_BALANCE)

    # Проверяем, хватает ли средств на ставку
    if current_balance < COST_PER_SPIN:
        return jsonify(
            {
                "error": "Недостаточно баллов для ставки!",
                "balance": current_balance,
            }
        ), 400

    # Списываем стоимость прокрута
    new_balance = current_balance - COST_PER_SPIN

    # Генерируем случайные символы для трех барабанов
    symbols_list = list(SYMBOLS.keys())
    result = [
        random.choice(symbols_list),
        random.choice(symbols_list),
        random.choice(symbols_list),
    ]

    won_amount = 0
    message = "Повезет в следующий раз!"

    # Проверяем на выигрыш (все три символа одинаковые)
    if result[0] == result[1] == result[2]:
        winning_symbol = result[0]
        won_amount = SYMBOLS[winning_symbol]
        new_balance += won_amount
        message = f"Поздравляем! Вы выиграли {won_amount} баллов!"

    return jsonify(
        {
            "result": result,
            "balance": new_balance,
            "won_amount": won_amount,
            "message": message,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
