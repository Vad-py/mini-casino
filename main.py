import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Общий баланс пользователя
user_balance = 2300

# Шаблон, объединяющий главное меню, слоты и новую рулетку на одной странице
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Игровой Портал</title>
    <style>
        body {
            background-color: #1a1a2e;
            color: #ffffff;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .container {
            margin-top: 50px;
        }
        /* Главное меню с иконками */
        #main-menu {
            display: flex;
            justify-content: center;
            gap: 50px;
            margin-top: 100px;
        }
        .game-card {
            background: #16213e;
            border: 2px solid #0f3460;
            border-radius: 15px;
            padding: 30px;
            width: 220px;
            cursor: pointer;
            transition: 0.3s;
        }
        .game-card:hover {
            transform: scale(1.05);
            border-color: #e94560;
        }
        .game-card h2 {
            margin-bottom: 10px;
            font-size: 22px;
        }
        
        /* Экраны игр */
        .game-screen {
            display: none;
        }
        .active {
            display: block;
        }
        
        .back-btn {
            background: #e94560;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
            font-size: 16px;
        }
        .back-btn:hover {
            background: #ff6b81;
        }

        .balance-box {
            font-size: 20px;
            background: #0f3460;
            display: inline-block;
            padding: 10px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        /* Стили для рулетки */
        .roulette-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            margin-top: 30px;
        }
        .wheel-container {
            position: relative;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: #111;
            border: 8px solid #ffd700;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }
        .wheel-center {
            font-size: 24px;
            font-weight: bold;
            background: #222;
            padding: 20px;
            border-radius: 50%;
            width: 100px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            border: 4px dashed #fff;
        }
        .ball {
            position: absolute;
            width: 15px;
            height: 15px;
            background: #fff;
            border-radius: 50%;
            box-shadow: 0 0 10px #fff;
            display: none;
        }
        .controls-panel {
            text-align: left;
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
        }
        .controls-panel label {
            display: block;
            margin: 10px 0 5px;
        }
        .controls-panel select, .controls-panel input {
            padding: 8px;
            width: 100%;
            background: #0f3460;
            color: #fff;
            border: 1px solid #e94560;
            border-radius: 5px;
            box-sizing: border-box;
        }
        .spin-btn {
            background: #e94560;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
            width: 100%;
        }
        .spin-btn:hover {
            background: #ff6b81;
        }

        /* Слоты */
        .slots-box {
            font-size: 50px;
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
            margin: 20px 0;
            border: 2px solid #0f3460;
        }
        .slot-spin-btn {
            background: #e94560;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .message {
            margin-top: 15px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="container">
        <!-- ГЛАВНОЕ МЕНЮ С ДВУМЯ ИКОНКАМИ -->
        <div id="main-menu" class="active">
            <div class="game-card" onclick="openScreen('slots-screen')">
                <h2>🎰 Мини-Казик</h2>
                <p>Классические слоты</p>
            </div>
            <div class="game-card" onclick="openScreen('roulette-screen')">
                <h2>🎡 Колесо Фортуны</h2>
                <p>Рулетка (Цвета и Числа x30)</p>
            </div>
        </div>

        <!-- ЭКРАН 1: СЛОТЫ -->
        <div id="slots-screen" class="game-screen">
            <button class="back-btn" onclick="openScreen('main-menu')">← Назад в меню</button>
            <h1>🎰 Мини-Казик</h1>
            <div class="balance-box">Баланс: <span id="slots-balance">{{ balance }}</span> баллов</div>
            <br>
            <div class="slots-box" id="slots-display">💎 🍋 🍋</div>
            <br>
            <button class="slot-spin-btn" onclick="spinSlots()">КРУТИТЬ (150)</button>
            <div class="message" id="slots-msg">Повесет в следующий раз!</div>
            
            <div style="margin-top: 30px; text-align: left; display: inline-block; background: #16213e; padding: 15px; border-radius: 8px;">
                <b>Правила:</b> Стоимость прокрута — 150 баллов.<br>
                🍒 🍒 🍒 = 100<br>
                🍋 🍋 🍋 = 250<br>
                💎 💎 💎 = 500
            </div>
        </div>

        <!-- ЭКРАН 2: КОЛЕСО ФОРТУНЫ -->
        <div id="roulette-screen" class="game-screen">
            <button class="back-btn" onclick="openScreen('main-menu')">← Назад в меню</button>
            <h1>🎡 Колесо Фортуны</h1>
            <div class="balance-box">Баланс: <span id="roulette-balance">{{ balance }}</span> баллов</div>
            
            <div class="roulette-wrapper">
                <!-- Колесо посередине -->
                <div class="wheel-container" id="wheel">
                    <div class="wheel-center" id="wheel-result-text">🎯</div>
                    <div class="ball" id="ball"></div>
                </div>

                <!-- Кнопки и панель управления чуть справа -->
                <div class="controls-panel">
                    <label>Сумма ставки:</label>
                    <select id="r-amount">
                        <option value="100">100 баллов</option>
                        <option value="250">250 баллов</option>
                        <option value="500">500 баллов</option>
                    </select>

                    <label>Тип ставки:</label>
                    <select id="r-type" onchange="changeBetType()">
                        <option value="color">На цвет (х1.5)</option>
                        <option value="number">На число (х30)</option>
                    </select>

                    <div id="color-choice-div">
                        <label>Выберите цвет:</label>
                        <select id="r-color">
                            <option value="red">Красный</option>
                            <option value="black">Черный</option>
                        </select>
                    </div>

                    <div id="number-choice-div" style="display: none;">
                        <label>Выберите число (1-30):</label>
                        <input type="number" id="r-number" min="1" max="30" value="15">
                    </div>

                    <button class="spin-btn" onclick="spinRoulette()">Бросить мячик</button>
                </div>
            </div>
            <div class="message" id="roulette-msg">Сделайте ставку и запустите колесо!</div>
        </div>
    </div>

    <script>
        function openScreen(screenId) {
            document.getElementById('main-menu').classList.remove('active');
            document.getElementById('slots-screen').classList.remove('active');
            document.getElementById('roulette-screen').classList.remove('active');
            document.getElementById(screenId).classList.add('active');
        }

        function changeBetType() {
            let type = document.getElementById('r-type').value;
            if (type === 'color') {
                document.getElementById('color-choice-div').style.display = 'block';
                document.getElementById('number-choice-div').style.display = 'none';
            } else {
                document.getElementById('color-choice-div').style.display = 'none';
                document.getElementById('number-choice-div').style.display = 'block';
            }
        }

        // Логика старых слотов
        function spinSlots() {
            fetch('/spin', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    document.getElementById('slots-msg').innerText = data.message;
                    return;
                }
                document.getElementById('slots-display').innerText = data.result.join(' ');
                document.getElementById('slots-balance').innerText = data.balance;
                document.getElementById('roulette-balance').innerText = data.balance;
                if (data.win > 0) {
                    document.getElementById('slots-msg').innerText = `Вы выиграли ${data.win} баллов!`;
                } else {
                    document.getElementById('slots-msg').innerText = 'Повезет в следующий раз!';
                }
            });
        }

        // Логика новой рулетки
        function spinRoulette() {
            let amount = document.getElementById('r-amount').value;
            let type = document.getElementById('r-type').value;
            let value = type === 'color' ? document.getElementById('r-color').value : document.getElementById('r-number').value;

            // Анимация броска мячика
            let ball = document.getElementById('ball');
            ball.style.display = 'block';
            ball.style.transition = '0s';
            ball.style.top = '10px';
            ball.style.left = '140px';
            
            setTimeout(() => {
                ball.style.transition = '1s ease-in-out';
                ball.style.top = `${Math.random() * 200 + 50}px`;
                ball.style.left = `${Math.random() * 200 + 50}px`;
            }, 50);

            fetch('/spin_roulette', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount: amount, type: type, value: value })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    document.getElementById('roulette-msg').innerText = data.message;
                    return;
                }
                setTimeout(() => {
                    document.getElementById('slots-balance').innerText = data.balance;
                    document.getElementById('roulette-balance').innerText = data.balance;
                    let centerText = document.getElementById('wheel-result-text');
                    centerText.innerText = data.number;
                    centerText.style.color = data.color === 'red' ? '#ff4757' : '#2ed573';
                    document.getElementById('roulette-msg').innerText = data.message;
                }, 1000);
            });
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  global user_balance
  return render_template_string(HTML_TEMPLATE, balance=user_balance)


@app.route("/spin", methods=["POST"])
def spin():
  global user_balance
  cost = 150

  if user_balance < cost:
    return jsonify({"success": False, "message": "Недостаточно баллов!"})

  user_balance -= cost
  symbols = ["🍒", "🍋", "💎"]
  result = [random.choice(symbols) for _ in range(3)]

  win = 0
  if result == ["🍒", "🍒", "🍒"]:
    win = 100
  elif result == ["🍋", "🍋", "🍋"]:
    win = 250
  elif result == ["💎", "💎", "💎"]:
    win = 500

  user_balance += win
  return jsonify({
      "success": True,
      "result": result,
      "win": win,
      "balance": user_balance,
  })


@app.route("/spin_roulette", methods=["POST"])
def spin_roulette():
  global user_balance
  data = request.json
  bet_amount = int(data.get("amount", 100))
  bet_type = data.get("type")
  bet_value = data.get("value")

  if user_balance < bet_amount:
    return jsonify({"success": False, "message": "Недостаточно баллов!"})

  user_balance -= bet_amount

  # 30 чисел рулетки (1-30), делим на красный и черный цвета (15 тех, 15 других)
  winning_number = random.randint(1, 30)
  winning_color = "red" if winning_number <= 15 else "black"

  win = 0
  message = f"Выпало число {winning_number} ({'Красное' if winning_color == 'red' else 'Черное'}). "

  if bet_type == "color":
    if bet_value == winning_color:
      # Увеличение на 50% (например, ставка 100 -> выплата 150)
      win = int(bet_amount * 1.5)
      message += f"Вы угадали цвет и выиграли {win} баллов!"
    else:
      message += "Вы проиграли ставку на цвет."

  elif bet_type == "number":
    if int(bet_value) == winning_number:
      # Увеличение в 30 раз
      win = bet_amount * 30
      message += (
          f"ДЖЕКПОТ! Вы угадали точное число и сорвали куш: {win} баллов!"
      )
    else:
      message += "Вы не угадали число."

  user_balance += win

  return jsonify({
      "success": True,
      "number": winning_number,
      "color": winning_color,
      "win": win,
      "balance": user_balance,
      "message": message,
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)