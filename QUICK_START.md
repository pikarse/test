# 🚀 Быстрый запуск

## 1. Подготовка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd hhhhh

# Убедитесь, что у вас Python 3.8+
python --version
```

## 2. Настройка бота

1. Создайте бота в Telegram через [@BotFather](https://t.me/BotFather)
2. Получите токен бота
3. Отредактируйте `bot/bot.py`:
   ```python
   API_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Вставьте ваш токен
   ```

## 3. Запуск

### Вариант 1: Автоматический запуск (рекомендуется)
```bash
python start.py
```

### Вариант 2: Ручной запуск

**Терминал 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Терминал 2 - Веб-сервер:**
```bash
cd webapp
python -m http.server 8080
```

**Терминал 3 - Бот:**
```bash
cd bot
pip install -r requirements.txt
python bot.py
```

## 4. Использование

1. Откройте Telegram
2. Найдите вашего бота
3. Отправьте `/start`
4. Выберите город
5. Нажмите "🗺 Открыть карту"
6. Добавляйте метки и комментарии!

## 5. Проверка работы

- Backend API: http://localhost:5000/api/stats
- WebApp: http://localhost:8080
- Бот: активен в Telegram

## 🛑 Остановка

Нажмите `Ctrl+C` в терминале с `start.py` или в каждом терминале отдельно.

---

**Проблемы?** Смотрите полную документацию в `README.md` 