#!/usr/bin/env python3
"""
Скрипт для запуска всех компонентов проекта
Telegram Bot - Карта России с метками и комментариями
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    """Вывод баннера проекта"""
    banner = """
    🗺 Telegram Bot - Карта России с метками и комментариями
    ========================================================
    
    🚀 Запуск всех компонентов...
    """
    print(banner)

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} - OK")

def install_requirements(requirements_file):
    """Установка зависимостей"""
    if os.path.exists(requirements_file):
        print(f"📦 Установка зависимостей из {requirements_file}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], 
                         check=True, capture_output=True)
            print(f"✅ Зависимости установлены")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки зависимостей: {e}")
            return False
    return True

def start_backend():
    """Запуск backend сервера"""
    print("🔧 Запуск Flask Backend...")
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Папка backend не найдена")
        return False
    
    # Установка зависимостей backend
    if not install_requirements("backend/requirements.txt"):
        return False
    
    # Запуск backend
    try:
        process = subprocess.Popen([sys.executable, "main.py"], 
                                 cwd=backend_dir,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        time.sleep(2)  # Даем время на запуск
        if process.poll() is None:
            print("✅ Backend запущен на http://localhost:5000")
            return process
        else:
            print("❌ Ошибка запуска backend")
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска backend: {e}")
        return False

def start_webapp():
    """Запуск веб-сервера для frontend"""
    print("🌐 Запуск веб-сервера для frontend...")
    webapp_dir = Path("webapp")
    if not webapp_dir.exists():
        print("❌ Папка webapp не найдена")
        return False
    
    try:
        process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"], 
                                 cwd=webapp_dir,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        time.sleep(1)
        if process.poll() is None:
            print("✅ Веб-сервер запущен на http://localhost:8080")
            return process
        else:
            print("❌ Ошибка запуска веб-сервера")
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска веб-сервера: {e}")
        return False

def start_bot():
    """Запуск Telegram бота"""
    print("🤖 Запуск Telegram бота...")
    bot_dir = Path("bot")
    if not bot_dir.exists():
        print("❌ Папка bot не найдена")
        return False
    
    # Проверка токена бота
    bot_file = bot_dir / "bot.py"
    if bot_file.exists():
        with open(bot_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'YOUR_BOT_TOKEN_HERE' in content:
                print("⚠️  ВНИМАНИЕ: Не забудьте установить токен бота в bot/bot.py")
                print("   Создайте бота через @BotFather и замените API_TOKEN")
                return False
    
    # Установка зависимостей bot
    if not install_requirements("bot/requirements.txt"):
        return False
    
    # Запуск бота
    try:
        process = subprocess.Popen([sys.executable, "bot.py"], 
                                 cwd=bot_dir,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        time.sleep(2)
        if process.poll() is None:
            print("✅ Telegram бот запущен")
            return process
        else:
            print("❌ Ошибка запуска бота")
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        return False

def main():
    """Основная функция"""
    print_banner()
    check_python_version()
    
    processes = []
    
    try:
        # Запуск backend
        backend_process = start_backend()
        if backend_process:
            processes.append(("Backend", backend_process))
        
        # Запуск веб-сервера
        webapp_process = start_webapp()
        if webapp_process:
            processes.append(("WebApp", webapp_process))
        
        # Запуск бота
        bot_process = start_bot()
        if bot_process:
            processes.append(("Bot", bot_process))
        
        if not processes:
            print("\n❌ Не удалось запустить ни одного компонента")
            return
        
        print("\n🎉 Все компоненты запущены!")
        print("\n📋 Доступные сервисы:")
        print("   • Backend API: http://localhost:5000")
        print("   • WebApp: http://localhost:8080")
        print("   • Telegram Bot: активен")
        
        print("\n📖 Инструкции:")
        print("   1. Откройте Telegram и найдите вашего бота")
        print("   2. Отправьте команду /start")
        print("   3. Выберите город и откройте карту")
        print("   4. Добавляйте метки и комментарии!")
        
        print("\n⏹  Для остановки нажмите Ctrl+C")
        
        # Ожидание завершения
        try:
            while True:
                time.sleep(1)
                # Проверяем, что все процессы еще работают
                for name, process in processes:
                    if process.poll() is not None:
                        print(f"\n❌ {name} неожиданно завершился")
                        return
        except KeyboardInterrupt:
            print("\n\n🛑 Остановка всех компонентов...")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Получен сигнал остановки")
    
    finally:
        # Остановка всех процессов
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} остановлен")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️  {name} принудительно остановлен")
            except Exception as e:
                print(f"❌ Ошибка остановки {name}: {e}")
        
        print("\n👋 Все компоненты остановлены")

if __name__ == "__main__":
    main() 