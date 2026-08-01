import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

user_balance = 1600

# Фиксированный порядок чисел на колесе
WHEEL_LAYOUT = [
    {"number": 23, "color": "red"}, {"number": 10, "color": "black"}, {"number": 5, "color": "red"},
    {"number": 27, "color": "black"}, {"number": 18, "color": "red"}, {"number": 24, "color": "black"},
    {"number": 16, "color": "red"}, {"number": 29, "color": "black"}, {"number": 4, "color": "red"},
    {"number": 17, "color": "black"}, {"number": 7, "color": "red"}, {"number": 22, "color": "black"},
    {"number": 12, "color": "red"}, {"number": 2, "color": "black"}, {"number": 25, "color": "red"},
    {"number": 14, "color": "black"}, {"number": 30, "color": "red"}, {"number": 9, "color": "black"},
    {"number": 3, "color": "red"}, {"number": 19, "color": "black"}, {"number": 11, "color": "red"},
    {"number": 26, "color": "black"}, {"number": 6, "color": "red"}, {"number": 33, "color": "black"},
    {"number": 15, "color": "red"}, {"number": 8, "color": "black"}, {"number": 20, "color": "red"},
    {"number": 1, "color": "black"}, {"number": 28, "color": "red"}, {"number": 13, "color": "black"}
]

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
            position: relative;
        }
        
        /* Главное меню */
        #main-menu {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 50px;
        }
        .menu-header {
            font-size: 36px;
            margin-bottom: 40px;
            color: #f8fafc;
        }
        .menu-cards {
            display: flex;
            justify-content: center;
            gap: 40px;
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

        /* Колесо Фортуны */
        .roulette-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 50px;
            margin-top: 20px;
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
            box-shadow: 0 2px 6px rgba(0,0,0,0.6);
            transform: translate(-50%, -50%);
        }
        .bg-red { background: #dc2626; border: 1px solid #fca5a5; }
        .bg-black { background: #111827; border: 2px solid #9ca3af; }
        .wheel-center {
            position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-size: 28px; font-weight: bold;
            background: #1e293b; color: #f8fafc;
            width: 110px; height: 110px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            border: 4px solid #f59e0b;
            box-shadow: 0 0 15px rgba(0,0,0,0.8); z-index: 5;
        }
        .ball {
            position: absolute; width: 18px; height: 18px;
            background: #ffffff; border-radius: 50%;
            box-shadow: 0 0 12px #ffffff, 0 0 5px #fffa65;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%); z-index: 10;
            display: none;
        }
        @keyframes spinBall {
            0% { transform: rotate(0deg) translate(185px) rotate(0deg); }
            100% { transform: rotate(1800deg) translate(185px) rotate(-1800deg); }
        }
        .spinning { display: block !important; animation: spinBall 5s cubic-bezier(0.15, 0.85, 0.35, 1.0) forwards; }

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
            padding: 10px; width: 100%;
            background: #0f172a; color: #fff;
            border: 1px solid #475569;
            border-radius: 8px; box-sizing: border-box;
            font-size: 15px;
        }
        .spin-btn {
            background: #f59e0b; color: #0f172a;
            border: none; padding: 14px 20px;
            font-size: 18px; font-weight: bold;
            border-radius: 10px; cursor: pointer;
            margin-top: 20px; width: 100%;
            transition: 0.2s;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }
        .spin-btn:hover { background: #fbbf24; transform: translateY(-2px); }
        .spin-btn:disabled { background: #64748b; cursor: not-allowed; transform: none; box-shadow: none; }

        .message {
            margin-top: 20px; font-size: 20px; font-weight: bold;
            min-height: 30px;
            position: absolute; bottom: 5px; left: 0; right: 0; text-align: center;
        }

        /* Правила для рулетки (сдвинуты влево) */
        .roulette-rules {
            position: absolute;
            top: 220px;
            left: -120px;
            width: 250px;
            background: #16213e;
            border: 1px solid #0f3460;
            border-radius: 10px;
            padding: 15px;
            text-align: left;
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.5;
        }
        .roulette-rules h4 { margin: 0 0 10px 0; color: #f8fafc; font-size: 16px; }

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
            background: #dc2626; color: white;
            border: none; padding: 15px 35px;
            font-size: 20px; font-weight: bold;
            border-radius: 10px; cursor: pointer;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
            transition: 0.2s;
        }
        .slot-spin-btn:hover { background: #ef4444; transform: translateY(-2px); }

        /* Правила для слотов (сдвинуты влево) */
        .slots-rules {
            margin-top: 25px;
            position: absolute;
            left: 50px;
            text-align: left;
            display: inline-block;
            background: #1e293b;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #334155;
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.6;
        }
    </style>
</head>
<body>

    <div class="container">
        <!-- ГЛАВНОЕ МЕНЮ -->
        <div id="main-menu" class="active">
            <h1 class="menu-header">🎰 Выберите игру</h1>
            <div class="menu-cards">
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
            
            <div class="message" id="slots-msg">Повесет в следующий раз!</div>
            
            <div class="slots-rules">
                <b>Правила игры:</b><br>
                Стоимость одного прокрута составляет 150 баллов.<br>
                Выпадение трех одинаковых символов приносит выигрыш:<br>
                🍒 🍒 🍒 = 100 баллов<br>
                🍋 🍋 🍋 = 250 баллов<br>
                💎 💎 💎 = 500 баллов
            </div>
        </div>

        <!-- ЭКРАН 2: КОЛЕСО ФОРТУНЫ -->
        <div id="roulette-screen" class="game-screen">
            <button class="back-btn" onclick="openScreen('main-menu')">← Назад в меню</button>
            <h1>🎡 Колесо Фортуны</h1>
            <div class="balance-box">Баланс: <span id="roulette-balance">{{ balance }}</span> баллов</div>
            
            <div class="roulette-rules">
                <h4>Правила игры:</h4>
                1. Выберите сумму ставки (100, 250, 500).<br>
                2. Выберите режим:<br>
                &nbsp;&nbsp;• *На цвет* (красный/черный): выигрыш х1.5 от ставки.<br>
            </div>
        </div>
    </div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, balance=user_balance)

@app.route('/spin_slots', methods=['POST'])
def spin_slots():
    global user_balance
    cost = 150
    if user_balance < cost:
        return jsonify({'error': 'Недостаточно баллов'}), 400
    
    user_balance -= cost
    symbols = ['🍒', '🍋', '💎']
    weights = [50, 35, 15]
    result = [random.choices(symbols, weights=weights)[0] for _ in range(3)]
    
    win = 0
    if result[0] == result[1] == result[2]:
        if result[0] == '🍒':
            win = 100
        elif result[0] == '🍋':
            win = 250
        elif result[0] == '💎':
            win = 500
            
    user_balance += win
    return jsonify({'result': result, 'win': win, 'balance': user_balance})

@app.route('/spin_roulette', methods=['POST'])
def spin_roulette():
    global user_balance
    data = request.get_json()
    bet = int(data.get('bet', 100))
    bet_type = data.get('type')
    bet_value = data.get('value')
    
    if user_balance < bet:
        return jsonify({'error': 'Недостаточно баллов'}), 400
        
    user_balance -= bet
    winning_sector = random.choice(WHEEL_LAYOUT)
    
    win = 0
    if bet_type == 'color':
        if winning_sector['color'] == bet_value:
            win = int(bet * 1.5)
    elif bet_type == 'number':
        if winning_sector['number'] == int(bet_value):
            win = bet * 30
            
    user_balance += win
    winning_index = WHEEL_LAYOUT.index(winning_sector)
    
    return jsonify({
        'sector': winning_sector,
        'index': winning_index,
        'win': win,
        'balance': user_balance
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)