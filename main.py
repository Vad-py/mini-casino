from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

user_balance = 1000.00

# Глобальное состояние игры Ракетка (Crash)
rocket_game_state = {
    "active": False,
    "bet": 0,
    "multiplier": 1.00,
    "crash_at": 1.00,
    "cashed_out": False
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Space Rocket Crash: Полное погружение</title>
    <style>
        :root {
            --bg-color: #0b0e14;
            --panel-bg: #151922;
            --accent-green: #0ecb81;
            --accent-red: #f6465d;
            --accent-yellow: #f0b90b;
            --text-main: #eaecef;
            --text-muted: #848e9c;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: var(--panel-bg);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border: 1px solid #2b313a;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #2b313a;
            padding-bottom: 12px;
            margin-bottom: 15px;
        }
        .balance {
            font-size: 1.1rem;
            font-weight: bold;
            color: var(--accent-green);
        }
        .game-screen {
            position: relative;
            height: 320px;
            background: linear-gradient(to bottom, #020617, #1e1b4b, #3b82f6);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            overflow: hidden;
            border: 1px solid #3b82f6;
            margin-bottom: 15px;
            padding-bottom: 25px;
            transition: background 1s ease;
        }
        .stars {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: radial-gradient(white 1px, transparent 0), radial-gradient(white 1px, transparent 0);
            background-size: 40px 40px;
            background-position: 0 0, 20px 20px;
            opacity: 0;
            transition: opacity 1s ease;
        }
        .earth-horizon {
            position: absolute;
            bottom: -150px;
            width: 200%;
            height: 180px;
            background: radial-gradient(ellipse at center, #1e3a8a 0%, #0f172a 70%);
            border-radius: 50%;
            border-top: 3px solid #60a5fa;
            transition: bottom 1s ease;
        }
        .rocket-container {
            position: relative;
            z-index: 5;
            transition: transform 0.1s linear;
        }
        .rocket-svg {
            width: 70px;
            height: 110px;
            filter: drop-shadow(0 0 10px rgba(255,165,0,0.7));
        }
        .flame {
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            width: 16px;
            height: 40px;
            background: linear-gradient(to bottom, #fde047, #f97316, transparent);
            border-radius: 50% 50% 20% 20%;
            animation: flicker 0.1s infinite alternate;
            filter: blur(2px);
        }
        @keyframes flicker {
            0% { transform: translateX(-50%) scaleY(1); opacity: 0.9; }
            100% { transform: translateX(-50%) scaleY(1.3); opacity: 1; }
        }
        .info-overlay {
            position: absolute;
            top: 15px;
            text-align: center;
            z-index: 10;
            width: 100%;
        }
        .multiplier {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: 2px;
            color: #fff;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        }
        .status-text {
            font-size: 0.85rem;
            color: #93c5fd;
            text-transform: uppercase;
            font-weight: 600;
            text-shadow: 0 1px 4px rgba(0,0,0,0.8);
        }
        .controls {
            display: grid;
            gap: 12px;
        }
        .input-group {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0b0e14;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #2b313a;
        }
        input[type="number"] {
            background: transparent;
            border: none;
            color: white;
            font-size: 1.1rem;
            width: 100px;
            text-align: right;
            outline: none;
        }
        button {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.1s, opacity 0.2s;
        }
        button:active { transform: scale(0.98); }
        .btn-start {
            background: var(--accent-green);
            color: #0b0e14;
        }
        .btn-cashout {
            background: var(--accent-yellow);
            color: #0b0e14;
            display: none;
            margin-top: 12px;
        }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .log-box {
            margin-top: 15px;
            background: #0b0e14;
            border-radius: 8px;
            padding: 10px;
            height: 70px;
            overflow-y: auto;
            font-size: 0.8rem;
            color: var(--text-muted);
            border: 1px solid #2b313a;
        }
        /* Блок правил игры */
        .rules-box {
            margin-top: 20px;
            background: #0b0e14;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #2b313a;
        }
        .rules-title {
            font-size: 0.95rem;
            font-weight: bold;
            color: var(--accent-yellow);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .rules-list {
            margin: 0;
            padding-left: 18px;
            font-size: 0.82rem;
            color: var(--text-muted);
            line-height: 1.5;
        }
        .rules-list li {
            margin-bottom: 6px;
        }
        .rules-list strong {
            color: var(--text-main);
        }
    </style>
</head>
<body>

<div class="container">
    <header>
        <div><strong>SPACE CRASH</strong> <span style="font-size:0.75rem; color:var(--text-muted);">Real Rocket Edition</span></div>
        <div class="balance">Баланс: <span id="balanceVal">{{ "%.2f"|format(balance) }}</span> USDT</div>
    </header>

    <div class="game-screen" id="gameScreen">
        <div class="stars" id="starsBg"></div>
        <div class="earth-horizon" id="earthHorizon"></div>

        <div class="info-overlay">
            <div class="multiplier" id="multiplierVal">1.00x</div>
            <div class="status-text" id="statusText">Космодром готов к пуску...</div>
        </div>

        <div class="rocket-container" id="rocketObj">
            <div class="flame" id="rocketFlame" style="display: none;"></div>
            <svg class="rocket-svg" viewBox="0 0 100 150" xmlns="http://www.w3.org/2000/svg">
                <path d="M50 5 Q35 30 35 60 L65 60 Q65 30 50 5 Z" fill="#f1f5f9"/>
                <rect x="35" y="60" width="30" height="60" fill="#e2e8f0"/>
                <circle cx="50" cy="80" r="8" fill="#0284c7" stroke="#94a3b8" stroke-width="3"/>
                <circle cx="48" cy="78" r="2" fill="#ffffff"/>
                <path d="M35 90 L15 120 L35 110 Z" fill="#ef4444"/>
                <path d="M65 90 L85 120 L65 110 Z" fill="#ef4444"/>
                <path d="M40 120 L60 120 L55 130 L45 130 Z" fill="#475569"/>
            </svg>
        </div>
    </div>

    <div class="controls" id="controlsBlock">
        <div class="input-group">
            <span>Ставка (USDT):</span>
            <input type="number" id="betInput" value="10" min="1" max="10000">
        </div>
        <button class="btn-start" onclick="startFlight()">ЗАПУСТИТЬ РАКЕТУ В КОСМОС</button>
    </div>

    <button class="btn-cashout" id="cashoutBtn" onclick="cashOut()">ЗАБРАТЬ (<span id="profitVal">0.00</span> USDT)</button>

    <div class="log-box" id="logBox">
        <div class="log-item">Системы корабля в норме. Ожидание старта.</div>
    </div>

    <!-- Информационный блок с правилами игры -->
    <div class="rules-box">
        <div class="rules-title">📜 Правила игры Space Crash</div>
        <ul class="rules-list">
            <li><strong>Суть игры:</strong> Ваша задача — запустить ракету в космос и успеть забрать выигрыш до того, как произойдет авария (крах).</li>
            <li><strong>Рост множителя:</strong> С каждой секундой полета коэффициент (множитель) увеличивается. Чем дольше летит ракета, тем больше потенциальный выигрыш.</li>
            <li><strong>Кэшаут (Забрать):</strong> Нажимайте кнопку «ЗАБРАТЬ» в процессе полета, пока ракета не взорвалась. Ваш выигрыш рассчитывается как: <code>Ставка × Текущий множитель</code>.</li>
            <li><strong>Риск аварии:</strong> Полет может завершиться внезапно в любой момент (крах). Если вы не успели нажать «Забрать» до взрыва, сумма ставки сгорает.</li>
        </ul>
    </div>
</div>

<script>
    let currentBet = 0;
    let currentMultiplier = 1.00;
    let gameInterval = null;
    let gameActive = false;
    let hasCashedOut = false;

    const balanceEl = document.getElementById('balanceVal');
    const multiplierEl = document.getElementById('multiplierVal');
    const rocketObj = document.getElementById('rocketObj');
    const rocketFlame = document.getElementById('rocketFlame');
    const statusTextEl = document.getElementById('statusText');
    const betInput = document.getElementById('betInput');
    const controlsBlock = document.getElementById('controlsBlock');
    const cashoutBtn = document.getElementById('cashoutBtn');
    const profitValEl = document.getElementById('profitVal');
    const logBox = document.getElementById('logBox');
    const gameScreen = document.getElementById('gameScreen');
    const starsBg = document.getElementById('starsBg');
    const earthHorizon = document.getElementById('earthHorizon');

    function log(text, color = '') {
        const div = document.createElement('div');
        div.className = 'log-item';
        if(color) div.style.color = color;
        div.innerText = `[${new Date().toLocaleTimeString()}] ${text}`;
        logBox.prepend(div);
    }

    function startFlight() {
        let bet = parseFloat(betInput.value);
        if (isNaN(bet) || bet <= 0) {
            alert('Неверная сумма ставки!');
            return;
        }

        fetch('/start_rocket', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ amount: bet })
        })
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                alert(data.message);
                return;
            }

            currentBet = bet;
            balanceEl.innerText = data.balance.toFixed(2);

            gameActive = true;
            hasCashedOut = false;
            currentMultiplier = 1.00;

            controlsBlock.style.display = 'none';
            cashoutBtn.style.display = 'block';
            multiplierEl.style.color = '#fff';
            rocketFlame.style.display = 'block';
            statusTextEl.innerText = 'Преодоление атмосферы...';
            log(`Ставка ${currentBet} USDT. Пуск ракеты!`);

            let startTime = Date.now();

            gameInterval = setInterval(() => {
                fetch('/check_rocket')
                .then(r => r.json())
                .then(statusData => {
                    if (!statusData.active) {
                        clearInterval(gameInterval);
                        if (gameActive && !hasCashedOut) {
                            gameActive = false;
                            currentMultiplier = statusData.multiplier;
                            endFlight(false);
                        }
                        return;
                    }

                    currentMultiplier = statusData.multiplier;
                    multiplierEl.innerText = currentMultiplier.toFixed(2) + 'x';
                    profitValEl.innerText = (currentBet * currentMultiplier).toFixed(2);

                    let elapsed = (Date.now() - startTime) / 1000;

                    if (currentMultiplier > 2.0) {
                        starsBg.style.opacity = '1';
                        earthHorizon.style.bottom = '-200px';
                        gameScreen.style.background = 'linear-gradient(to bottom, #000000, #090d16, #1e1b4b)';
                        statusTextEl.innerText = 'ВЫХОД В ОТКРЫТЫЙ КОСМОС';
                    }

                    let lift = Math.min(elapsed * 12, 100);
                    let tilt = Math.sin(elapsed * 6) * 4;
                    rocketObj.style.transform = `translateY(-${lift}px) rotate(${tilt}deg)`;
                });
            }, 100);
        });
    }

    function cashOut() {
        if (!gameActive || hasCashedOut) return;
        
        fetch('/cashout_rocket', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (!data.success) return;

            hasCashedOut = true;
            clearInterval(gameInterval);
            gameActive = false;
            
            balanceEl.innerText = data.balance.toFixed(2);
            multiplierEl.style.color = 'var(--accent-green)';
            statusTextEl.innerText = 'УСПЕШНЫЙ КЭШАУТ!';
            log(`Успех! Ракета принесла ${data.win.toFixed(2)} USDT на х${data.multiplier.toFixed(2)}`, 'var(--accent-green)');

            endFlight(true);
        });
    }

    function endFlight(success) {
        rocketFlame.style.display = 'none';
        multiplierEl.innerText = currentMultiplier.toFixed(2) + 'x';

        if (!success) {
            rocketObj.style.transform = 'translateY(20px) rotate(90deg)';
            multiplierEl.style.color = 'var(--accent-red)';
            statusTextEl.innerText = 'АВАРИЯ РАКЕТЫ (КРАХ)!';
            log(`Взрыв на орбите (х${currentMultiplier.toFixed(2)}). Потеряно ${currentBet} USDT`, 'var(--accent-red)');
        }

        cashoutBtn.style.display = 'none';
        controlsBlock.style.display = 'grid';

        setTimeout(() => {
            rocketObj.style.transform = 'translateY(0px) rotate(0deg)';
            starsBg.style.opacity = '0';
            earthHorizon.style.bottom = '-150px';
            gameScreen.style.background = 'linear-gradient(to bottom, #020617, #1e1b4b, #3b82f6)';
        }, 2500);
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, balance=user_balance)

@app.route('/start_rocket', methods=['POST'])
def start_rocket():
    global user_balance, rocket_game_state
    data = request.json
    amount = float(data.get('amount', 10))

    if user_balance < amount:
        return jsonify({"success": False, "message": "Недостаточно средств!"})

    user_balance -= amount
    crash_target = round(1.01 + (random.random() * random.random() * 15), 2)

    rocket_game_state = {
        "active": True,
        "bet": amount,
        "multiplier": 1.00,
        "crash_at": crash_target,
        "cashed_out": False
    }

    return jsonify({"success": True, "balance": user_balance})

@app.route('/check_rocket', methods=['GET'])
def check_rocket():
    global rocket_game_state
    if not rocket_game_state["active"]:
        return jsonify({"active": False, "multiplier": rocket_game_state["multiplier"]})

    rocket_game_state["multiplier"] += 0.04
    rocket_game_state["multiplier"] = round(rocket_game_state["multiplier"], 2)

    if rocket_game_state["multiplier"] >= rocket_game_state["crash_at"]:
        rocket_game_state["multiplier"] = rocket_game_state["crash_at"]
        rocket_game_state["active"] = False
        return jsonify({"active": False, "multiplier": rocket_game_state["multiplier"]})

    return jsonify({
        "active": True,
        "multiplier": rocket_game_state["multiplier"]
    })

@app.route('/cashout_rocket', methods=['POST'])
def cashout_rocket():
    global user_balance, rocket_game_state
    if not rocket_game_state["active"] or rocket_game_state["cashed_out"]:
        return jsonify({"success": False, "message": "Уже поздно"})

    rocket_game_state["cashed_out"] = True
    rocket_game_state["active"] = False

    win = rocket_game_state["bet"] * rocket_game_state["multiplier"]
    user_balance += win

    return jsonify({
        "success": True,
        "balance": user_balance,
        "win": win,
        "multiplier": rocket_game_state["multiplier"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)