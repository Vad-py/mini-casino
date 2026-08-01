import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

user_balance = 2500

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
            position: relative;
        }
        .container {
            max-width: 950px;
            margin: 0 auto;
            position: relative;
        }
        
        /* Главное меню */
        #main-menu {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 30px;
        }
        .menu-header {
            font-size: 36px;
            margin-bottom: 30px;
            color: #f8fafc;
        }
        .menu-cards {
            display: flex;
            justify-content: center;
            gap: 25px;
            flex-wrap: wrap;
        }
        .game-card {
            background: #1e293b;
            border: 3px solid #334155;
            border-radius: 20px;
            padding: 30px 20px;
            width: 240px;
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
            font-size: 22px;
            margin-bottom: 10px;
            color: #f8fafc;
        }
        .game-card p {
            color: #94a3b8;
            font-size: 14px;
        }

        /* Экраны игр */
        .game-screen {
            display: none;
            position: relative;
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
            margin-bottom: 20px;
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
            margin-bottom: 20px;
            border: 2px solid #334155;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        /* Обертка для экрана слотов */
        .slots-layout {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 30px;
            margin-top: 10px;
        }
        .slots-center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .slots-rules {
            width: 240px;
            background: #16213e;
            border: 1px solid #0f3460;
            border-radius: 12px;
            padding: 15px;
            text-align: left;
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.5;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .slots-rules h4 { margin: 0 0 8px 0; color: #f8fafc; font-size: 15px; }

        /* Колесо Фортуны */
        .roulette-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            margin-top: 10px;
        }
        .wheel-container {
            position: relative;
            width: 450px;
            height: 450px;
            min-width: 450px;
            min-height: 450px;
            border-radius: 50%;
            background: #090d16;
            border: 12px solid #b45309;
            box-sizing: border-box;
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
            text-align: center;
        }

        .roulette-rules {
            width: 240px;
            background: #16213e;
            border: 1px solid #0f3460;
            border-radius: 12px;
            padding: 15px;
            text-align: left;
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.5;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .roulette-rules h4 { margin: 0 0 8px 0; color: #f8fafc; font-size: 15px; }

        /* Слоты */
        .slots-box {
            font-size: 65px;
            background: #1e293b;
            padding: 30px;
            border-radius: 16px;
            display: inline-block;
            margin: 15px 0;
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
        .slot-spin-btn:disabled { background: #64748b; cursor: not-allowed; transform: none; box-shadow: none; }

        /* Стили для игры "Мины" */
        .mines-wrapper {
            display: flex;
            justify-content: center;
            gap: 35px;
            align-items: flex-start;
        }
        .mines-panel {
            width: 440px;
            background: #1e293b;
            border-radius: 16px;
            padding: 24px;
            border: 2px solid #334155;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            text-align: left;
        }
        .mines-info-panel {
            display: flex;
            justify-content: space-between;
            background: #0f1923;
            padding: 12px 18px;
            border-radius: 10px;
            margin-bottom: 18px;
            font-size: 1rem;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-bottom: 18px;
        }
        .cell {
            aspect-ratio: 1;
            background: #334155;
            border: none;
            border-radius: 10px;
            font-size: 2rem;
            font-weight: 900;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .cell:hover:not(:disabled) { background: #475569; }
        .cell:active:not(:disabled) { transform: scale(0.95); }
        .cell.gem {
            background: rgba(245, 158, 11, 0.25);
            border: 2px solid #f59e0b;
            color: #f59e0b;
            text-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
        }
        .cell.mine {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid #ef4444;
        }
        .controls {
            display: grid;
            gap: 12px;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .control-group label {
            font-size: 0.9rem;
            color: #94a3b8;
        }
        .control-group input, .control-group select {
            background: #0f1923;
            border: 1px solid #334155;
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-size: 1rem;
            width: 100%;
            box-sizing: border-box;
        }
        button.action-btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.1s;
        }
        button.action-btn:active { transform: scale(0.98); }
        .btn-start { background: #10b981; color: #0f1923; }
        .btn-cashout { background: #f59e0b; color: #0f1923; display: none; margin-top: 15px; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }

        /* Полноэкранный салют для джекпота */
        #fireworks-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 9999;
            display: none;
            overflow: hidden;
        }
        .firework-particle {
            position: absolute;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: explode 1s ease-out forwards;
        }
        @keyframes explode {
            0% {
                transform: translate(0, 0) scale(1);
                opacity: 1;
            }
            100% {
                transform: translate(var(--dx), var(--dy)) scale(0.2);
                opacity: 0;
            }
        }
    </style>
</head>
<body>

    <!-- Полноэкранный контейнер для салютов -->
    <div id="fireworks-overlay"></div>

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
                <div class="game-card" onclick="openScreen('mines-screen')">
                    <h2>💣 Мины</h2>
                    <p>Сапер на криптовалюту</p>
                </div>
            </div>
        </div>

        <!-- ЭКРАН 1: СЛОТЫ -->
        <div id="slots-screen" class="game-screen">
            <button class="back-btn" onclick="openScreen('main-menu')">← Назад в меню</button>
            <h1>🎰 Мини-Казик</h1>
            <div class="balance-box">Баланс: <span id="slots-balance">{{ balance }}</span> гривень</div>
            
            <div class="slots-layout">
                <div class="slots-rules">
                    <h4>Правила игры:</h4>
                    Стоимость прокрута: 150 гривень.<br><br>
                    Комбинации:<br>
                    🍒 🍒 🍒 = 100 гривень<br>
                    🍋 🍋 🍋 = 250 гривень<br>
                    💎 💎 💎 = 500 гривень
                </div>

                <div class="slots-center-content">
                    <div class="slots-box" id="slots-display">💎 🍋 🍋</div>
                    <button class="slot-spin-btn" id="slot-btn" onclick="spinSlots()">КРУТИТЬ (150)</button>
                    <div class="message" id="slots-msg" style="margin-top: 15px;">Повезет в следующий раз!</div>
                </div>
            </div>
        </div>

        <!-- ЭКРАН 2: КОЛЕСО ФОРТУНЫ -->
        <div id="roulette-screen" class="game-screen">
            <button class="back-btn" onclick="openScreen('main-menu')">← Назад в меню</button>
            <h1>🎡 Колесо Фортуны</h1>
            <div class="balance-box">Баланс: <span id="roulette-balance">{{ balance }}</span> гривень</div>
            
            <div class="roulette-wrapper">
                <div class="roulette-rules">
                    <h4>Правила игры:</h4>
                    1. Выберите ставку (100, 250, 500).<br>
                    2. Выберите режим:<br>
                    &nbsp;&nbsp;• <b>На цвет</b>: х1.5<br>
                    &nbsp;&nbsp;• <b>На число</b>: х30
                </div>

                <div class="wheel-container" id="wheel">
                    <div class="wheel-center" id="wheel-result-text">🎯</div>
                    <div class="ball" id="ball"></div>
                </div>

                <div class="controls-panel">
                    <label>Сумма ставки:</label>
                    <select id="r-amount">
                        <option value="100">100 гривень</option>
                        <option value="250">250 гривень</option>
                        <option value="500">500 гривень</option>
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
                        <input type="number" id="r-number" min="1" max="30" value="23">
                    </div>

                    <button class="spin-btn" id="r-spin-btn" onclick="spinRoulette()">Бросить мячик</button>
                </div>
            </div>
            <div class="message" id="roulette-msg" style="margin-top: 20px;">Сделайте ставку и запустите колесо!</div>
        </div>

        <!-- ЭКРАН 3: МИНЫ -->
        <div id="mines-screen" class="game-screen">
            <button class="back-btn" onclick="openScreen('main-menu')">← Назад в меню</button>
            <h1>💣 Игра «Мины»</h1>
            <div class="balance-box">Баланс: <span id="mines-balance">{{ balance }}</span> гривень</div>

            <div class="mines-wrapper">
                <div class="slots-rules" style="margin-right: 10px;">
                    <h4>Правила игры:</h4>
                    1. Выберите ставку и количество мин.<br>
                    2. Открывайте биткоины (₿), избегая мин (💣).<br>
                    3. Больше мин — выше множитель за каждый шаг!<br>
                    4. Заберите выигрыш в любой момент кнопкой «ЗАБРАТЬ».
                </div>

                <div class="mines-panel">
                    <div class="mines-info-panel">
                        <div>Множитель: <strong id="multiplierVal" style="color: #f59e0b;">1.00x</strong></div>
                        <div>Выигрыш: <strong id="potentialWin" style="color: #10b981;">0.00 гривень</strong></div>
                    </div>

                    <!-- Игровое поле 5x5 -->
                    <div class="grid" id="minesGrid"></div>

                    <div class="controls" id="controlsBlock">
                        <div class="control-group">
                            <label>Сумма ставки (гривень):</label>
                            <input type="number" id="betInput" value="100" min="1" max="10000">
                        </div>
                        <div class="control-group">
                            <label>Количество мин:</label>
                            <select id="minesCount">
                                <option value="1">1 мина (старт х1.02)</option>
                                <option value="3" selected>3 мины (старт х1.11)</option>
                                <option value="5">5 мин (старт х1.23)</option>
                                <option value="10">10 мин (старт х1.65)</option>
                                <option value="15">15 мин (старт х2.47)</option>
                            </select>
                        </div>
                        <button class="action-btn btn-start" onclick="startMinesGame()">ИГРАТЬ</button>
                    </div>

                    <button class="action-btn btn-cashout" id="cashoutBtn" onclick="cashOutMines()">ЗАБРАТЬ <span id="cashoutAmount">0.00</span> гривень</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const wheelLayout = {{ layout | tojson }};

        // --- WEB AUDIO API ДЛЯ ВСЕХ ЗВУКОВ ---
        let audioCtx = null;
        function getAudioContext() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            return audioCtx;
        }

        // 1. Звук прокрута слотов (быстрый механический треск)
        function playSlotSpinSound() {
            try {
                let ctx = getAudioContext();
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(150, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(40, ctx.currentTime + 0.05);
                gain.gain.setValueAtTime(0.1, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.05);
            } catch(e) {}
        }

        // 2. Идеальный синхронный звук тиканья колеса фортуны
        function playTickSound() {
            try {
                let ctx = getAudioContext();
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(750, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(180, ctx.currentTime + 0.035);
                gain.gain.setValueAtTime(0.12, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.035);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.035);
            } catch(e) {}
        }

        // 3. НОВЫЙ МОЩНЫЙ И СОЧНЫЙ ЗВУК ВЫИГРЫША (Яркий победный аккорд с арпеджио и большей громкостью)
        function playWinSound() {
            try {
                let ctx = getAudioContext();
                let now = ctx.currentTime;
                let notes = [523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98];
                notes.forEach((freq, index) => {
                    let osc = ctx.createOscillator();
                    let gain = ctx.createGain();
                    
                    osc.type = index % 2 === 0 ? 'triangle' : 'sine';
                    osc.frequency.setValueAtTime(freq, now + index * 0.06);
                    
                    gain.gain.setValueAtTime(0, now + index * 0.06);
                    gain.gain.linearRampToValueAtTime(0.28, now + index * 0.06 + 0.02);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + index * 0.06 + 0.6);
                    
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + index * 0.06);
                    osc.stop(now + index * 0.06 + 0.6);
                });
            } catch(e) {}
        }

        // 4. Общий звук проигрыша
        function playLoseSound() {
            try {
                let ctx = getAudioContext();
                let now = ctx.currentTime;
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(220, now);
                osc.frequency.exponentialRampToValueAtTime(110, now + 0.5);
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.5);
            } catch(e) {}
        }

        // 5. Звук успеха в Минах (обычный шаг)
        function playMinesSuccessSound() {
            try {
                let ctx = getAudioContext();
                let now = ctx.currentTime;
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(440, now);
                osc.frequency.exponentialRampToValueAtTime(880, now + 0.12);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.15);
            } catch(e) {}
        }

        // 6. Звук провала в Минах (попадание на бомбу)
        function playMinesBombSound() {
            try {
                let ctx = getAudioContext();
                let now = ctx.currentTime;
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(120, now);
                osc.frequency.exponentialRampToValueAtTime(30, now + 0.4);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.4);
            } catch(e) {}
        }

        // 7. Звук взрывов салютов/фейерверков (серия басовых хлопков и свиста в течение 5 секунд)
        function playFireworksSound() {
            try {
                let ctx = getAudioContext();
                let startTime = ctx.currentTime;
                
                // Запускаем несколько серий взрывов в течение 5 секунд
                for (let i = 0; i < 12; i++) {
                    let delay = i * 0.4 + Math.random() * 0.15;
                    let explosionTime = startTime + delay;
                    
                    // Белый шум для звука взрыва / хлопка
                    let bufferSize = ctx.sampleRate * 0.4;
                    let buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                    let data = buffer.getChannelData(0);
                    for (let j = 0; j < bufferSize; j++) {
                        data[j] = Math.random() * 2 - 1;
                    }
                    
                    let noise = ctx.createBufferSource();
                    noise.buffer = buffer;
                    
                    let filter = ctx.createBiquadFilter();
                    filter.type = 'lowpass';
                    filter.frequency.setValueAtTime(800, explosionTime);
                    filter.frequency.exponentialRampToValueAtTime(100, explosionTime + 0.35);
                    
                    let gain = ctx.createGain();
                    gain.gain.setValueAtTime(0.4, explosionTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, explosionTime + 0.38);
                    
                    noise.connect(filter);
                    filter.connect(gain);
                    gain.connect(ctx.destination);
                    
                    noise.start(explosionTime);
                    noise.stop(explosionTime + 0.38);
                }
            } catch(e) {}
        }
        // ---------------------------------------------------

        function formatMoney(amount) {
            let parts = amount.toFixed(2).split('.');
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            return parts.join(',');
        }

        function updateAllBalances(newBalance) {
            let formatted = formatMoney(newBalance);
            document.getElementById('slots-balance').innerText = formatted;
            document.getElementById('roulette-balance').innerText = formatted;
            document.getElementById('mines-balance').innerText = formatted;
        }

        window.onload = function() {
            const wheel = document.getElementById('wheel');
            const totalNumbers = wheelLayout.length;
            const radius = 168;

            wheelLayout.forEach((item, index) => {
                const angle = index * (360 / totalNumbers) * (Math.PI / 180);
                const x = 213 + radius * Math.cos(angle);
                const y = 213 + radius * Math.sin(angle);

                const numDiv = document.createElement('div');
                numDiv.className = 'wheel-number ' + (item.color === 'red' ? 'bg-red' : 'bg-black');
                numDiv.innerText = item.number;
                numDiv.style.left = x + 'px';
                numDiv.style.top = y + 'px';
                numDiv.id = 'num-' + item.number;
                wheel.appendChild(numDiv);
            });

            updateAllBalances({{ balance }});
            initMinesGrid();
        };

        function openScreen(screenId) {
            document.getElementById('main-menu').classList.remove('active');
            document.getElementById('slots-screen').classList.remove('active');
            document.getElementById('roulette-screen').classList.remove('active');
            document.getElementById('mines-screen').classList.remove('active');
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

        // Функция запуска анимации салютов на 5 секунд
        function triggerFireworks() {
            const overlay = document.getElementById('fireworks-overlay');
            overlay.style.display = 'block';
            overlay.innerHTML = '';

            let colors = ['#f59e0b', '#ef4444', '#10b981', '#3b82f6', '#ec4899', '#8b5cf6', '#ffffff'];

            // Создаем несколько залпов салюта в течение 4 секунд
            let burstInterval = setInterval(() => {
                let startX = Math.random() * window.innerWidth;
                let startY = window.innerHeight * 0.2 + Math.random() * (window.innerHeight * 0.5);
                let particleCount = 40;

                for (let i = 0; i < particleCount; i++) {
                    let particle = document.createElement('div');
                    particle.className = 'firework-particle';
                    particle.style.left = startX + 'px';
                    particle.style.top = startY + 'px';
                    particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

                    let angle = Math.random() * Math.PI * 2;
                    let speed = 50 + Math.random() * 180;
                    let dx = Math.cos(angle) * speed;
                    let dy = Math.sin(angle) * speed;

                    particle.style.setProperty('--dx', dx + 'px');
                    particle.style.setProperty('--dy', dy + 'px');

                    overlay.appendChild(particle);

                    setTimeout(() => {
                        particle.remove();
                    }, 1000);
                }
            }, 400);

            // Через 5 секунд полностью очищаем и скрываем контейнер
            setTimeout(() => {
                clearInterval(burstInterval);
                overlay.style.display = 'none';
                overlay.innerHTML = '';
            }, 5000);
        }

        function spinSlots() {
            let slotBtn = document.getElementById('slot-btn');
            slotBtn.disabled = true;
            document.getElementById('slots-msg').innerText = 'Крутим слоты...';

            let symbols = ["🍒", "🍋", "💎"];
            let display = document.getElementById('slots-display');
            
            let counter = 0;
            let animInterval = setInterval(() => {
                let tempRes = [
                    symbols[Math.floor(Math.random() * symbols.length)],
                    symbols[Math.floor(Math.random() * symbols.length)],
                    symbols[Math.floor(Math.random() * symbols.length)]
                ];
                display.innerText = tempRes.join(' ');
                playSlotSpinSound();
                counter++;
                if (counter > 15) {
                    clearInterval(animInterval);
                    
                    fetch('/spin', { method: 'POST' })
                    .then(res => res.json())
                    .then(data => {
                        slotBtn.disabled = false;
                        if (!data.success) {
                            document.getElementById('slots-msg').innerText = data.message;
                            return;
                        }
                        display.innerText = data.result.join(' ');
                        updateAllBalances(data.balance);
                        
                        if (data.win > 0) {
                            document.getElementById('slots-msg').innerText = `Вы выиграли ${formatMoney(data.win)} гривень!`;
                            playWinSound();
                        } else {
                            document.getElementById('slots-msg').innerText = 'Повезет в следующий раз!';
                            playLoseSound();
                        }
                    });
                }
            }, 80);
        }

        function spinRoulette() {
            let amount = document.getElementById('r-amount').value;
            let type = document.getElementById('r-type').value;
            let value = type === 'color' ? document.getElementById('r-color').value : document.getElementById('r-number').value;

            let spinBtn = document.getElementById('r-spin-btn');
            spinBtn.disabled = true;
            document.getElementById('roulette-msg').innerText = 'Мячик запущен, крутится...';

            let ball = document.getElementById('ball');
            ball.style.display = 'none';
            ball.style.animation = 'none';

            fetch('/spin_roulette', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount: amount, type: type, value: value })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    spinBtn.disabled = false;
                    document.getElementById('roulette-msg').innerText = data.message;
                    return;
                }

                let winningIndex = wheelLayout.findIndex(item => item.number === data.number);
                let totalNumbers = wheelLayout.length;
                let anglePerItem = 360 / totalNumbers;
                let targetAngle = 1800 + (winningIndex * anglePerItem);

                ball.style.display = 'block';
                ball.offsetHeight;
                
                let styleSheet = document.styleSheets[0];
                for (let i = 0; i < styleSheet.cssRules.length; i++) {
                    if (styleSheet.cssRules[i].name === 'spinBall') {
                        styleSheet.deleteRule(i);
                        break;
                    }
                }
                styleSheet.insertRule(`
                    @keyframes spinBall {
                        0% { transform: translate(-50%, -50%) rotate(0deg) translate(168px) rotate(0deg); }
                        100% { transform: translate(-50%, -50%) rotate(${targetAngle}deg) translate(168px) rotate(-${targetAngle}deg); }
                    }
                `, styleSheet.cssRules.length);

                ball.style.animation = `spinBall 5s cubic-bezier(0.15, 0.85, 0.35, 1.0) forwards`;

                let startTime = performance.now();
                let duration = 5000;
                let lastTickedAngle = -1;
                let sectorAngle = 360 / totalNumbers;

                function trackBallTicks(currentTime) {
                    let elapsed = currentTime - startTime;
                    let progress = Math.min(elapsed / duration, 1.0);
                    let easeProgress = 1 - Math.pow(1 - progress, 3);
                    let currentAngle = targetAngle * easeProgress;
                    
                    let sectorIndex = Math.floor(currentAngle / sectorAngle);
                    if (sectorIndex > lastTickedAngle) {
                        playTickSound();
                        lastTickedAngle = sectorIndex;
                    }

                    if (progress < 1.0) {
                        requestAnimationFrame(trackBallTicks);
                    }
                }
                requestAnimationFrame(trackBallTicks);

                setTimeout(() => {
                    ball.style.display = 'none';
                    updateAllBalances(data.balance);
                    
                    let centerText = document.getElementById('wheel-result-text');
                    centerText.innerText = data.number;
                    centerText.style.color = data.color === 'red' ? '#dc2626' : '#9ca3af';
                    
                    document.getElementById('roulette-msg').innerText = data.message;
                    spinBtn.disabled = false;

                    if (data.win > 0) {
                        playWinSound();
                        // Если ставка была на точное число и она сыграла — запускаем салюты и звук взрывов на 5 секунд
                        if (type === 'number' && parseInt(value) === data.number) {
                            triggerFireworks();
                            playFireworksSound();
                        }
                    } else {
                        playLoseSound();
                    }
                }, 5000);
            });
        }

        let minesGameActive = false;
        let currentMinesBet = 100;
        let totalCells = 25;

        const minesGrid = document.getElementById('minesGrid');
        const controlsBlock = document.getElementById('controlsBlock');
        const cashoutBtn = document.getElementById('cashoutBtn');
        const multiplierEl = document.getElementById('multiplierVal');
        const potentialWinEl = document.getElementById('potentialWin');
        const cashoutAmountEl = document.getElementById('cashoutAmount');
        const betInput = document.getElementById('betInput');
        const minesCountSelect = document.getElementById('minesCount');

        function initMinesGrid() {
            minesGrid.innerHTML = '';
            for (let i = 0; i < totalCells; i++) {
                const cell = document.createElement('button');
                cell.className = 'cell';
                cell.dataset.index = i;
                cell.disabled = true;
                cell.onclick = () => clickMinesCell(i);
                minesGrid.appendChild(cell);
            }
        }

        function startMinesGame() {
            let bet = parseFloat(betInput.value);
            let mCount = parseInt(minesCountSelect.value);
            
            let rawBalanceText = document.getElementById('mines-balance').innerText.replace(/\./g, '').replace(',', '.');
            let globalBalance = parseFloat(rawBalanceText);

            if (isNaN(bet) || bet <= 0 || bet > globalBalance) {
                alert('Неверная сумма ставки!');
                return;
            }

            currentMinesBet = bet;

            fetch('/start_mines', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount: bet, mines: mCount })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    alert(data.message);
                    return;
                }

                updateAllBalances(data.balance);
                minesGameActive = true;
                
                multiplierEl.innerText = '1.00x';
                potentialWinEl.innerText = formatMoney(currentMinesBet) + ' гривень';
                cashoutAmountEl.innerText = formatMoney(currentMinesBet);

                const cells = document.querySelectorAll('#minesGrid .cell');
                cells.forEach(cell => {
                    cell.className = 'cell';
                    cell.innerText = '';
                    cell.disabled = false;
                });

                controlsBlock.style.display = 'none';
                cashoutBtn.style.display = 'block';
            });
        }

        function clickMinesCell(index) {
            if (!minesGameActive) return;
            const cell = minesGrid.children[index];
            if (cell.disabled || cell.classList.contains('gem') || cell.classList.contains('mine')) return;

            cell.disabled = true;

            fetch('/click_mines', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index: index })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) return;

                if (data.hit_mine) {
                    cell.classList.add('mine');
                    cell.innerText = '💣';
                    playMinesBombSound();
                    endMinesGame(false, data.mines_list);
                } else {
                    cell.classList.add('gem');
                    cell.innerText = '₿';
                    playMinesSuccessSound();
                    
                    multiplierEl.innerText = data.multiplier.toFixed(2) + 'x';
                    
                    let winAmount = currentMinesBet * data.multiplier;
                    potentialWinEl.innerText = formatMoney(winAmount) + ' гривень';
                    cashoutAmountEl.innerText = formatMoney(winAmount);

                    if (data.won_auto) {
                        cashOutMines(true);
                    }
                }
            });
        }

        function cashOutMines(isAuto = false) {
            if (!minesGameActive) return;

            fetch('/cashout_mines', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (!data.success) return;

                updateAllBalances(data.balance);
                revealAllMines(data.mines_list);
                minesGameActive = false;
                cashoutBtn.style.display = 'none';
                controlsBlock.style.display = 'grid';

                playWinSound();

                if (!isAuto) {
                    potentialWinEl.innerText = `Забрано: ${formatMoney(data.win)} гривень`;
                }
            });
        }

        function endMinesGame(won, minesList) {
            minesGameActive = false;
            revealAllMines(minesList);
            cashoutBtn.style.display = 'none';
            controlsBlock.style.display = 'grid';
            if (!won) {
                potentialWinEl.innerText = 'ПОРАЖЕНИЕ (Мина)';
            }
        }

        function revealAllMines(minesList) {
            const cells = document.querySelectorAll('#minesGrid .cell');
            cells.forEach((cell, idx) => {
                cell.disabled = true;
                if (minesList.includes(idx)) {
                    cell.classList.add('mine');
                    cell.innerText = '💣';
                } else if (!cell.classList.contains('gem')) {
                    cell.style.opacity = '0.4';
                    cell.innerText = '₿';
                }
            });
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  global user_balance
  user_balance = 2500.0
  return render_template_string(
      HTML_TEMPLATE, balance=user_balance, layout=WHEEL_LAYOUT
  )


@app.route("/spin", methods=["POST"])
def spin():
  global user_balance
  cost = 150.0
  if user_balance < cost:
    return jsonify({"success": False, "message": "Недостаточно гривень!"})

  user_balance -= cost
  symbols = ["🍒", "🍋", "💎"]
  result = [random.choice(symbols) for _ in range(3)]

  win = 0.0
  if result == ["🍒", "🍒", "🍒"]:
    win = 100.0
  elif result == ["🍋", "🍋", "🍋"]:
    win = 250.0
  elif result == ["💎", "💎", "💎"]:
    win = 500.0

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
  bet_amount = float(data.get("amount", 100))
  bet_type = data.get("type")
  bet_value = data.get("value")

  if user_balance < bet_amount:
    return jsonify({"success": False, "message": "Недостаточно гривень!"})

  user_balance -= bet_amount

  winning_sector = random.choice(WHEEL_LAYOUT)
  winning_number = winning_sector["number"]
  winning_color = winning_sector["color"]

  win = 0.0
  color_name = "красное" if winning_color == "red" else "черное"
  message = f"Выпало число {winning_number} ({color_name}). "

  if bet_type == "color":
    if bet_value == winning_color:
      win = bet_amount * 1.5
      message += f"Вы угадали цвет и выиграли {win:.2f} гривень!"
    else:
      message += "Вы не угадали, смена на заводе ждет тебя!"

  elif bet_type == "number":
    if int(bet_value) == winning_number:
      win = bet_amount * 30
      message += f"ДЖЕКПОТ! Вы угадали точное число и сорвали куш: {win:.2f} гривень!"
    else:
      message += "Вы не угадали, смена на заводе ждет тебя!"

  user_balance += win

  return jsonify({
      "success": True,
      "number": winning_number,
      "color": winning_color,
      "win": win,
      "balance": user_balance,
      "message": message,
  })


START_MULTIPLIERS = {1: 1.02, 3: 1.11, 5: 1.23, 10: 1.65, 15: 2.47}


def calculate_multiplier(mines_count, revealed_count):
  if revealed_count == 0:
    return 1.0
  base_mult = START_MULTIPLIERS.get(mines_count, 1.11)
  if revealed_count == 1:
    return base_mult

  mult = base_mult
  total_cells = 25
  for i in range(1, revealed_count):
    safe_remaining = total_cells - mines_count - i
    total_remaining = total_cells - i
    if safe_remaining > 0:
      step_prob = safe_remaining / total_remaining
      mult *= (1.0 / step_prob) * 0.99
  return mult


mines_session = {
    "active": False,
    "bet": 0.0,
    "mines": 0,
    "mine_positions": [],
    "revealed": 0,
}


@app.route("/start_mines", methods=["POST"])
def start_mines():
  global user_balance, mines_session
  data = request.json
  bet = float(data.get("amount", 100))
  mines_count = int(data.get("mines", 3))

  if user_balance < bet:
    return jsonify({"success": False, "message": "Недостаточно гривень!"})

  user_balance -= bet

  mine_positions = []
  while len(mine_positions) < mines_count:
    rnd = random.randint(0, 24)
    if rnd not in mine_positions:
      mine_positions.append(rnd)

  mines_session = {
      "active": True,
      "bet": bet,
      "mines": mines_count,
      "mine_positions": mine_positions,
      "revealed": 0,
  }

  return jsonify(
      {"success": True, "balance": user_balance, "multiplier": 1.0}
  )


@app.route("/click_mines", methods=["POST"])
def click_mines():
  global user_balance, mines_session
  if not mines_session["active"]:
    return jsonify({"success": False})

  data = request.json
  index = int(data.get("index"))

  if index in mines_session["mine_positions"]:
    mines_session["active"] = False
    return jsonify({
        "success": True,
        "hit_mine": True,
        "mines_list": mines_session["mine_positions"],
    })

  mines_session["revealed"] += 1
  revealed = mines_session["revealed"]
  mines_count = mines_session["mines"]

  mult = calculate_multiplier(mines_count, revealed)

  safe_total = 25 - mines_count
  won_auto = revealed == safe_total
  if won_auto:
    win_amount = mines_session["bet"] * mult
    user_balance += win_amount
    mines_session["active"] = False

  return jsonify({
      "success": True,
      "hit_mine": False,
      "multiplier": mult,
      "won_auto": won_auto,
      "mines_list": mines_session["mine_positions"] if won_auto else [],
  })


@app.route("/cashout_mines", methods=["POST"])
def cashout_mines():
  global user_balance, mines_session
  if not mines_session["active"] or mines_session["revealed"] == 0:
    return jsonify({"success": False})

  revealed = mines_session["revealed"]
  mines_count = mines_session["mines"]

  mult = calculate_multiplier(mines_count, revealed)
  win_amount = mines_session["bet"] * mult
  user_balance += win_amount
  mines_session["active"] = False

  return jsonify({
      "success": True,
      "balance": user_balance,
      "win": win_amount,
      "mines_list": mines_session["mine_positions"],
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)