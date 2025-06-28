#!/usr/bin/env python3
"""
Веб-сервер для раздачи статических файлов приложения
"""

from flask import Flask, send_from_directory, render_template_string
import os
import requests

app = Flask(__name__)

# Получаем URL backend из переменной окружения
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')

# HTML шаблон для главной страницы
MAIN_PAGE_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Карта России - Веб-приложение</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.3);
            max-width: 500px;
            width: 90%;
        }

        .logo {
            font-size: 48px;
            margin-bottom: 20px;
        }

        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 28px;
        }

        .description {
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }

        .features {
            text-align: left;
            margin-bottom: 30px;
            color: #555;
        }

        .features ul {
            list-style: none;
            padding: 0;
        }

        .features li {
            padding: 8px 0;
            position: relative;
            padding-left: 25px;
        }

        .features li:before {
            content: "✅";
            position: absolute;
            left: 0;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            margin: 10px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }

        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            font-size: 14px;
        }

        .status.online {
            background: rgba(40, 167, 69, 0.1);
            color: #28a745;
            border: 1px solid rgba(40, 167, 69, 0.3);
        }

        .status.offline {
            background: rgba(220, 53, 69, 0.1);
            color: #dc3545;
            border: 1px solid rgba(220, 53, 69, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🗺️</div>
        <h1>Карта России</h1>
        <p class="description">
            Интерактивная карта с возможностью добавления меток, комментариев и отслеживания маршрутов
        </p>
        
        <div class="features">
            <ul>
                <li>Добавление меток с комментариями и рейтингами</li>
                <li>Отслеживание маршрутов в реальном времени</li>
                <li>Геолокация пользователя</li>
                <li>Редактирование и удаление меток/комментариев</li>
                <li>Время жизни меток и маршрутов</li>
            </ul>
        </div>

        <a href="/app" class="btn">🚀 Открыть приложение</a>
        <a href="/api/stats" class="btn btn-secondary" target="_blank">📊 API Статистика</a>
        
        <div class="status online" id="status">
            ✅ Сервер работает
        </div>
    </div>

    <script>
        // Проверка статуса API
        async function checkAPIStatus() {
            try {
                const response = await fetch('/api/stats');
                if (response.ok) {
                    document.getElementById('status').className = 'status online';
                    document.getElementById('status').textContent = '✅ Сервер работает';
                } else {
                    throw new Error('API недоступен');
                }
            } catch (error) {
                document.getElementById('status').className = 'status offline';
                document.getElementById('status').textContent = '❌ Сервер недоступен';
            }
        }

        // Проверяем статус при загрузке
        checkAPIStatus();
        
        // Проверяем каждые 30 секунд
        setInterval(checkAPIStatus, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Главная страница"""
    return render_template_string(MAIN_PAGE_HTML)

@app.route('/app')
def app_page():
    """Страница приложения"""
    return send_from_directory('webapp', 'index.html')

@app.route('/app/<path:filename>')
def app_files(filename):
    """Статические файлы приложения"""
    return send_from_directory('webapp', filename)

@app.route('/api/<path:path>')
def api_proxy(path):
    """Прокси для API запросов к backend"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/{path}')
        return response.text, response.status_code, response.headers.items()
    except:
        return {'error': 'Backend недоступен'}, 503

@app.route('/health')
def health_check():
    """Проверка здоровья сервиса"""
    return {'status': 'ok', 'service': 'russia-map-frontend', 'backend_url': BACKEND_URL}

if __name__ == '__main__':
    # Получаем порт из переменной окружения или используем 3000
    port = int(os.environ.get('PORT', 3000))
    
    print(f"🌐 Веб-сервер запущен на http://localhost:{port}")
    print(f"📱 Приложение доступно по адресу: http://localhost:{port}/app")
    print(f"🔧 API доступен по адресу: {BACKEND_URL}/api/")
    
    app.run(host='0.0.0.0', port=port, debug=False) 