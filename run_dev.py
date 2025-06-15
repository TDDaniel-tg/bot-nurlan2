#!/usr/bin/env python3
"""
Скрипт для запуска бота в режиме разработки
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Добавляем корневую директорию в Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Импортируем после добавления в path
from main import main
from config.settings import TELEGRAM_BOT_TOKEN, CLOUDCONVERT_API_KEY

def check_environment():
    """Проверка настроек окружения"""
    missing_vars = []
    
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == 'your_telegram_bot_token_here':
        missing_vars.append('TELEGRAM_BOT_TOKEN')
    
    if not CLOUDCONVERT_API_KEY or CLOUDCONVERT_API_KEY == 'your_cloudconvert_api_key_here':
        missing_vars.append('CLOUDCONVERT_API_KEY')
    
    if missing_vars:
        print("❌ Ошибка: Не настроены следующие переменные окружения:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Создайте файл .env на основе env.example и заполните необходимые значения.")
        return False
    
    return True

def setup_dev_logging():
    """Настройка расширенного логирования для разработки"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot_dev.log', encoding='utf-8')
        ]
    )

if __name__ == "__main__":
    print("🚀 Запуск PDF to Excel Converter Bot (Development Mode)")
    print("=" * 60)
    
    # Проверка окружения
    if not check_environment():
        sys.exit(1)
    
    # Настройка логирования
    setup_dev_logging()
    
    print("✅ Переменные окружения настроены")
    print("📝 Логирование включено (DEBUG режим)")
    print("🔄 Запускаем бота...")
    print("\n💡 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1) 