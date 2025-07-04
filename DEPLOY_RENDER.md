# 🚀 Деплой на Render.com

## 📋 Пошаговая инструкция

### 1. Подготовка репозитория

1. **Создайте репозиторий на GitHub**
2. **Загрузите все файлы проекта**
3. **Убедитесь, что есть все необходимые файлы:**
   - `render.yaml` - конфигурация для Render
   - `requirements.txt` - зависимости Python
   - `backend/main.py` - Backend API
   - `server.py` - Frontend сервер
   - `webapp/index.html` - Приложение

### 2. Создание сервисов на Render

#### Backend API:
1. **Перейдите на** [render.com](https://render.com)
2. **Нажмите** "New +" → "Web Service"
3. **Подключите** ваш GitHub репозиторий
4. **Настройте:**
   - **Name:** `russia-map-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && python main.py`
   - **Port:** `5000`

#### Frontend:
1. **Нажмите** "New +" → "Web Service"
2. **Выберите** тот же репозиторий
3. **Настройте:**
   - **Name:** `russia-map-frontend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install flask requests`
   - **Start Command:** `python server.py`
   - **Port:** `3000`

### 3. Настройка переменных окружения

#### Для Frontend сервиса:
1. **Перейдите** в настройки сервиса
2. **Найдите** раздел "Environment Variables"
3. **Добавьте:**
   - **Key:** `BACKEND_URL`
   - **Value:** `https://russia-map-backend.onrender.com`

### 4. Деплой

1. **Нажмите** "Create Web Service"
2. **Дождитесь** завершения сборки (5-10 минут)
3. **Проверьте** логи на наличие ошибок

## 🌐 Результат

После успешного деплоя:

- **Frontend:** `https://russia-map-frontend.onrender.com`
- **Backend:** `https://russia-map-backend.onrender.com`
- **Приложение:** `https://russia-map-frontend.onrender.com/app`

## 🔧 Проверка работы

1. **Откройте** главную страницу frontend
2. **Нажмите** "🚀 Открыть приложение"
3. **Проверьте** все функции:
   - Добавление меток
   - Комментарии
   - Редактирование
   - Маршруты

## ⚠️ Важные замечания

### Render Free Tier ограничения:
- **Сервисы "засыпают"** после 15 минут неактивности
- **Первая загрузка** может занять 30-60 секунд
- **Ограничения** на количество запросов

### Для production:
- **Обновите** на платный план
- **Настройте** базу данных (PostgreSQL)
- **Добавьте** SSL сертификаты
- **Настройте** CDN для статических файлов

## 🐛 Решение проблем

### Сервис не запускается:
1. **Проверьте** логи в Render Dashboard
2. **Убедитесь** что все зависимости установлены
3. **Проверьте** правильность команд запуска

### API недоступен:
1. **Проверьте** переменную `BACKEND_URL`
2. **Убедитесь** что backend сервис запущен
3. **Проверьте** CORS настройки

### Статические файлы не загружаются:
1. **Проверьте** структуру папок
2. **Убедитесь** что `webapp/` папка существует
3. **Проверьте** права доступа к файлам

## 📞 Поддержка

Если возникли проблемы:
1. **Проверьте** логи в Render Dashboard
2. **Обратитесь** в поддержку Render
3. **Проверьте** документацию Flask

---

**Удачи с деплоем!** 🚀 