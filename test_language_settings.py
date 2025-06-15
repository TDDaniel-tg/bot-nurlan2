#!/usr/bin/env python3
"""
Тест языковых настроек CloudConvert
"""

import os
from dotenv import load_dotenv
from config.settings import CLOUDCONVERT_OCR_LANGUAGES, CLOUDCONVERT_LOCALE

load_dotenv()

def test_language_settings():
    """Тестирование языковых настроек"""
    print("🌍 Проверка языковых настроек CloudConvert:")
    print(f"📝 OCR языки: {CLOUDCONVERT_OCR_LANGUAGES}")
    print(f"🌐 Локаль: {CLOUDCONVERT_LOCALE}")
    
    # Проверяем что русский язык включен
    if 'rus' in CLOUDCONVERT_OCR_LANGUAGES:
        print("✅ Русский язык для OCR включен")
    else:
        print("❌ Русский язык для OCR НЕ включен")
    
    # Проверяем локаль
    if CLOUDCONVERT_LOCALE.startswith('ru'):
        print("✅ Русская локаль настроена")
    else:
        print("⚠️ Русская локаль не настроена")
    
    print("\n🔧 Эти настройки будут использованы CloudConvert для:")
    print("   - Улучшенного распознавания русского текста")
    print("   - Правильного форматирования дат и чисел")
    print("   - Сохранения кириллических символов")
    
    print("\n📋 Для изменения настроек отредактируйте .env файл:")
    print("   CLOUDCONVERT_OCR_LANGUAGES=rus,eng  # Добавьте/уберите языки")
    print("   CLOUDCONVERT_LOCALE=ru_RU           # Измените локаль")

if __name__ == "__main__":
    test_language_settings() 