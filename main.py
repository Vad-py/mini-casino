<!DOCTYPE html>
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
        
        /* Блок с 4 иконками (меню/разделы) */
        .nav-icons-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 15px;
        }
        .nav-item {
            background: #0b0e14;
            border: 1px solid #2b313a;
            border-radius: 10px;
            padding: 8px 4px;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.2s, background 0.2s;
        }
        .nav-item:hover, .nav-item.active {
            border-color: var(--accent-green);
            background: #121824;
        }
        .nav-icon {
            font-size: 1.3rem;
            margin-bottom: 4px;
        }
        .nav-title {
            font-size: 0.75rem;
            font-weight: bold;
            color: var(--text-main);
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .nav-desc {
            font-size: 0.55rem;
            color: var(--text-muted);
            line-height: 1.1;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        /* Космический экран с динамическим фоном */
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
        /* Звезды в космосе */
        .stars {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: radial-gradient(white 1px, transparent 0), radial-gradient(white 1px, transparent 0);
            background-size: 40px 40px;
            background-position: 0 0, 20px 20px;
            opacity: 0;
            transition: opacity 1s ease;
        }
        /* Земля внизу для эффекта высоты */
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
        /* Ракета SVG */
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
        /* Огонь из сопла */
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
    </style>
</head>
<body>

<div class="container">
    <header>
        <div><strong>SPACE CRASH</strong> <span style="font-size:0.75rem; color:var(--text-muted);">Real Rocket Edition</span></div>
        <div class="balance">Баланс: <span id="balanceVal">1000.00</span> USDT</div>
    </header>

    <!-- Блок из 4 иконок посередине (включая 4-ю «Ракетка») -->
    <div class="nav-icons-grid">
        <div class="nav-item">
            <div class="nav-icon">🪐</div>
            <div class="nav-title">Орбита</div>
            <div class="nav-desc">Стандартный режим полета</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">☄️</div>
            <div class="nav-title">Метеор</div>
            <div class="nav-desc">Быстрые раунды</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">🛸</div>
            <div class="nav-title">Космос</div>
            <div class="nav-desc">Повышенный риск</div>
        </div>
        <div class="nav-item active">
            <div class="nav-icon">🚀</div>
            <div class="nav-title">Ракетка</div>
            <div class="nav-desc">Мы не рискуем, мы не входим в азарт, поставили - забрали</div>
        </div>
    </div>

    <div class="game-screen" id="gameScreen">
        <div class="stars" id="starsBg"></div>
        <div class="earth-horizon" id="earthHorizon"></div>

        <div class="info-overlay">
            <div class="multiplier" id="multiplierVal">1.00x</div>
            <div class="status-text" id="statusText">Космодром готов к пуску...</div>
        </div>

        <div class="rocket-container" id="rocketObj">
            <div class="flame" id="rocketFlame" style="display: none;"></div>
            <!-- Настоящая качественная векторная ракета вместо смайлика -->
            <svg class="rocket-svg" viewBox="0 0 100 150" xmlns="http://www.w3.org/2000/svg">
                <!-- Обтекатель носа -->
                <path d="M50 5 Q35 30 35 60 L65 60 Q65 30 50 5 Z" fill="#f1f5f9"/>
                <!-- Корпус -->
                <rect x="35" y="60" width="30" height="60" fill="#e2e8f0"/>
                <!-- Окно иллюминатора -->
                <circle cx="50" cy="80" r="8" fill="#0284c7" stroke="#94a3b8" stroke-width="3"/>
                <circle cx="48" cy="78" r="2" fill="#ffffff"/>
                <!-- Левое крыло -->
                <path d="M35 90 L15 120 L35 110 Z" fill="#ef4444"/>
                <!-- Правое крыло -->
                <path d="M65 90 L85 120 L65 110 Z" fill="#ef4444"/>
                <!-- Сопло двигателя -->
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
</div>

<script>
    let balance = 1000.00;
    let currentBet = 0;
    let currentMultiplier = 1.00;
    let crashPoint = 1.00;
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

    function calculateCrash() {
        if (Math.random() < 0.05) return 1.00;
        let crash = 1.01 + (Math.random() * Math.random() * 18);
        if (Math.random() < 0.03) crash = 25.0 + Math.random() * 75;
        return parseFloat(crash.toFixed(2));
    }

    function startFlight() {
        let bet = parseFloat(betInput.value);
        if (isNaN(bet) || bet <= 0 || bet > balance) {
            alert('Неверная сумма ставки!');
            return;
        }

        currentBet = bet;
        balance -= currentBet;
        balanceEl.innerText = balance.toFixed(2);

        gameActive = true;
        hasCashedOut = false;
        currentMultiplier = 1.00;
        crashPoint = calculateCrash();

        controlsBlock.style.display = 'none';
        cashoutBtn.style.display = 'block';
        multiplierEl.style.color = '#fff';
        rocketFlame.style.display = 'block';
        statusTextEl.innerText = 'Преодоление атмосферы...';
        log(`Ставка ${currentBet} USDT. Пуск ракеты!`);

        let startTime = Date.now();

        gameInterval = setInterval(() => {
            let elapsed = (Date.now() - startTime) / 1000;
            currentMultiplier = 1.00 + (elapsed * elapsed * 0.09) + (elapsed * 0.06);
            currentMultiplier = parseFloat(currentMultiplier.toFixed(2));

            // Динамический эффект выхода в открытый космос по мере роста иксов
            if (currentMultiplier > 2.0) {
                starsBg.style.opacity = '1';
                earthHorizon.style.bottom = '-200px';
                gameScreen.style.background = 'linear-gradient(to bottom, #000000, #090d16, #1e1b4b)';
                statusTextEl.innerText = 'ВЫХОД В ОТКРЫТЫЙ КОСМОС';
            }

            if (currentMultiplier >= crashPoint) {
                currentMultiplier = crashPoint;
                endFlight(false);
            } else {
                multiplierEl.innerText = currentMultiplier.toFixed(2) + 'x';
                profitValEl.innerText = (currentBet * currentMultiplier).toFixed(2);
                
                // Плавное покачивание и подъем ракеты на экране
                let lift = Math.min(elapsed * 12, 100);
                let tilt = Math.sin(elapsed * 6) * 4;
                rocketObj.style.transform = `translateY(-${lift}px) rotate(${tilt}deg)`;
            }
        }, 50);
    }

    function cashOut() {
        if (!gameActive || hasCashedOut) return;
        hasCashedOut = true;
        
        let winAmount = currentBet * currentMultiplier;
        balance += winAmount;
        balanceEl.innerText = balance.toFixed(2);

        multiplierEl.style.color = 'var(--accent-green)';
        statusTextEl.innerText = 'УСПЕШНЫЙ КЭШАУТ!';
        log(`Успех! Ракета принесла ${winAmount.toFixed(2)} USDT на х${currentMultiplier.toFixed(2)}`, 'var(--accent-green)');

        endFlight(true);
    }

    function endFlight(success) {
        clearInterval(gameInterval);
        gameActive = false;
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