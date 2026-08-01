import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Общий баланс пользователя
user_balance = 2300

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Игровой Портал</title>
    <style>
        body {
            background-color: #0f172a;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        /* Главное меню */
        #main-menu {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 150px;
        }
        .game-card {
            background: #1e293b;
            border: 3px solid #334155;
            border-radius: 20px;
            padding: 40px;
            width: 280px;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .game-card:hover {
            transform: translateY(-8px);
            border-color: #f59e0b;
            box-shadow: 0 15px 35px rgba(245, 158, 11, 0.3);
        }
        .game-card h2 {
            font-size: 26px;
            margin-bottom: 10px;
            color: #f8fafc;
        }
        .game-card p {
            color: #94a3b8;
            font-size: 16px;
        }

        /* Экраны игр */
        .game-screen {
            display: none;
        }
        .active {
            display: block;
        }
        
        .back-btn {
            background: #334155;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            cursor: pointer;
            margin-bottom: 25px;
            font-size: 16px;
            font-weight: bold;
            transition: 0.2s;
        }
        .back-btn:hover {
            background: #475569;
        }

        .balance-box {
            font-size: 22px;
            font-weight: bold;
            background: #1e293b;
            color: #f59e0b;
            display: inline-block;
            padding: 12px 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            border: 2px solid #334155;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        /* Крупное Колесо Фортуны */
        .roulette-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 50px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .wheel-container {
            position: relative;
            width: 450px;
            height: 450px;
            border-radius: 50%;
            background: #090d16;
            border: 12px solid #b45309;
            box-shadow: 0 0 40px rgba(180, 83, 9, 0.6), inset 0 0 30px rgba(0,0,0,0.8);
        }
        
        /* Цифры на колесе */
        .wheel-number {
            position: absolute;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: bold;
            color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.5);
            transform: translate(-50%, -50%);
        }
        .bg-red { background: #dc2626; }
        .bg-black { background: #1e293b; border: 1px solid #475569; }

        /* Центр колеса */
        .wheel-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 28px;
            font-weight: bold;
            background: #1e293b;
            color: #f8fafc;
            width: 110px;
            height: 110px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 4px solid #f59e0b;
            box-shadow: 0 0 15px rgba(0,0,0,0.8);
            z-index: 5;
        }

        /* Мячик с плавной анимацией вращения */
        .ball {
            position: absolute;
            width: 18px;
            height: 18px;
            background: #ffffff;
            border-radius: 50%;
            box-shadow: 0 0 12px #ffffff, 0 0 5px #fffa65;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10;
            display: none;
        }

        @keyframes spinBall {
            0% {
                transform: rotate(0deg) translate(185px) rotate(0deg);
            }
            100% {
                transform: rotate(1800deg) translate(185px) rotate(-1800deg); /* 5 полных оборотов + точное попадание */
            }
        }

        .spinning {
            display: block !important;
            animation: spinBall 5s cubic-bezier(0.15, 0.85, 0.35, 1.0) forwards;
        }

        /* Панель управления справа */
        .controls-panel {
            text-align: left;
            background: #1e293b;
            padding: 25px;
            border-radius: 16px;
            border: 2px solid #334155;
            width: 280px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }
        .controls-panel label {
            display: block;
            margin: 12px 0 6px;
            color: #cbd5e1;
            font-weight: 600;
        }
        .controls-panel select, .controls-panel input {
            padding: 10px;
            width: 100%;
            background: #0f172a;
            color: #fff;
            border: 1px solid #475569;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 15px;
        }
        .spin-btn {
            background: #f59e0b;
            color: #0f172a;
            border: none;
            padding: 14px 20px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
            transition: 0.2s;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }
        .spin-btn:hover {
            background: #fbbf24;
            transform: translateY(-2px);
        }
        .spin-btn:disabled {
            background: #64748b;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        /* Сообщения и результаты */
        .message {
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            min-height: 30px;
        }

        /* Слоты */
        .slots-box {
            font-size: 65px;
            background: #1e293b;
            padding: 30px;
            border-radius: 16px;
            display: inline-block;
            margin: 20px 0;
            border: 2px solid #334155;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }
        .slot-spin-btn {
            background: #dc2626;
            color: white;
            border: none;
            padding: 15px 35px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
            transition: 0.2s;
        }
        .slot-spin-btn:hover {
            background: #ef4444;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <div class="container">
        <!-- ГЛАВНОЕ МЕНЮ С ДВУМЯ ИКОНКАМИ -->
        <div id="main-menu" class="active">
            <h1 style="font-size: 36px; margin-bottom: 40px; color: #f8fafc;">🎰 Выберите игру</h1>
            <div style="display: flex; justify-content: center; gap: 40px;">
                <div class="game-card" onclick="openScreen('slots-screen')">
                    <h2>🎰 Мини-Казик</h2>
                    <p>Классические слоты</p>
                </div>
                <div class="game-card" onclick="openScreen('roulette-screen')">
                    <h2>🎡 Колесо Фортуны</h2>
                    <p>Рулетка (Цвета и Числа x30)</p>
                </div>
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
            <div class="message" id="slots-msg">Повезет в следующий раз!</div>
            
            <div style="margin-top: 35px; text-align: left; display: inline-block; background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
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
                <!-- Большое колесо с 30 числами по кругу -->
                <div class="wheel-container" id="wheel">
                    <div class="wheel-center" id="wheel-result-text">🎯</div>
                    <div class="ball" id="ball"></div>
                </div>

                <!-- Панель управления справа -->
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

                    <button class="spin-btn" id="r-spin-btn" onclick="spinRoulette()">Бросить мячик</button>
                </div>
            </div>
            <div class="message" id="roulette-msg">Сделайте ставку и запустите колесо!</div>
        </div>
    </div>

    <script>
        // Генерация 30 чисел по кругу рулетки при загрузке страницы
        window.onload = function() {
            const wheel = document.getElementById('wheel');
            const totalNumbers = 30;
            const radius = 185; // радиус от центра колеса

            for (let i = 1; i <= totalNumbers; i++) {
                const angle = (i - 1) * (360 / totalNumbers) * (Math.PI / 180);
                const x = 225 + radius * Math.cos(angle);
                const y = 225 + radius * Math.sin(angle);

                const numDiv = document.createElement('div');
                numDiv.className = 'wheel-number ' + (i <= 15 ? 'bg-red' : 'bg-black');
                numDiv.innerText = i;
                numDiv.style.left = x + 'px';
                numDiv.style.top = y + 'px';
                numDiv.id = 'num-' + i;
                wheel.appendChild(numDiv);
            }
        };

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

        // Логика новой рулетки с анимацией 5 секунд
        function spinRoulette() {
            let amount = document.getElementById('r-amount').value;
            let type = document.getElementById('r-type').value;
            let value = type === 'color' ? document.getElementById('r-color').value : document.getElementById('r-number').value;

            let spinBtn = document.getElementById('r-spin-btn');
            spinBtn.disabled = true;
            document.getElementById('roulette-msg').innerText = 'Мячик запущен, крутится... (5 сек)';

            let ball = document.getElementById('ball');
            ball.classList.remove('spinning');
            void ball.offsetWidth; // сброс анимации
            ball.classList.add('spinning');

            fetch('/spin_roulette', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount: amount, type: type, value: value })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    ball.classList.remove('spinning');
                    spinBtn.disabled = false;
                    document.getElementById('roulette-msg').innerText = data.message;
                    return;
                }

                // Ровно через 5 секунд останавливаем анимацию и выводим результат
                setTimeout(() => {
                    ball.classList.remove('spinning');
                    
                    // Позиционируем шарик прямо на выпавшем числе
                    const targetEl = document.getElementById('num-' + data.number);
                    if (targetEl) {
                        ball.style.top = targetEl.style.top;
                        ball.style.left = targetEl.style.left;
                        ball.style.display = 'block';
                    }

                    document.getElementById('slots-balance').innerText = data.balance;
                    document.getElementById('roulette-balance').innerText = data.balance;
                    
                    let centerText = document.getElementById('wheel-result-text');
                    centerText.innerText = data.number;
                    centerText.style.color = data.color === 'red' ? '#dc2626' : '#22c55e';
                    
                    document.getElementById('roulette-msg').innerText = data.message;
                    spinBtn.disabled = false;
                }, 5000);
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

  winning_number = random.randint(1, 30)
  winning_color = "red" if winning_number <= 15 else "black"

  win = 0
  message = f"Выпало число {winning_number} ({'Красное' if winning_color == 'red' else 'Черное'}). "

  if bet_type == "color":
    if bet_value == winning_color:
      win = int(bet_amount * 1.5)
      message += f"Вы угадали цвет и выиграли {win} баллов!"
    else:
      message += "Вы проиграли ставку на цвет."

  elif bet_type == "number":
    if int(bet_value) == winning_number:
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