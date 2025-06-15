#!/usr/bin/env python3
"""
Скрипт управления Claude AI для Telegram бота
Позволяет включать/выключать Claude AI и тестировать функции
"""

import os
import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent))

from config.settings import CLAUDE_API_KEY, CLAUDE_ENABLED, CLAUDE_MODEL
from services.text_enhancer import TextEnhancer

def update_env_variable(var_name: str, value: str):
    """Обновляет переменную окружения в .env файле"""
    env_path = Path('.env')
    
    if not env_path.exists():
        # Создаем .env файл если его нет
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(f"{var_name}={value}\n")
        return
    
    # Читаем существующий файл
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Обновляем или добавляем переменную
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{var_name}="):
            lines[i] = f"{var_name}={value}\n"
            updated = True
            break
    
    if not updated:
        lines.append(f"{var_name}={value}\n")
    
    # Записываем обратно
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def show_status():
    """Показывает текущий статус Claude AI"""
    print("🤖 Claude AI Status")
    print("=" * 40)
    print(f"API Key: {'✅ Настроен' if CLAUDE_API_KEY else '❌ Не настроен'}")
    print(f"Model: {CLAUDE_MODEL if CLAUDE_API_KEY else 'Не доступен'}")
    print(f"Status: {'🟢 Включен' if CLAUDE_ENABLED else '🔴 Отключен'}")
    print()

def enable_claude():
    """Включает Claude AI"""
    if not CLAUDE_API_KEY:
        print("❌ Ошибка: API ключ Claude не настроен!")
        print("Добавьте CLAUDE_API_KEY в файл .env")
        return
    
    update_env_variable('CLAUDE_MANUAL_ENABLED', 'true')
    print("✅ Claude AI включен!")
    print("Перезапустите бота для применения изменений.")

def disable_claude():
    """Отключает Claude AI"""
    update_env_variable('CLAUDE_MANUAL_ENABLED', 'false')
    print("🔴 Claude AI отключен!")
    print("Перезапустите бота для применения изменений.")

async def test_enhancement():
    """Тестирует функцию улучшения текста"""
    if not CLAUDE_ENABLED:
        print("❌ Claude AI не включен!")
        return
    
    print("🧪 Тестирование улучшения текста...")
    
    # Тестовый текст с ошибками OCR
    test_text = """
    Пр0ект пл4на pаз5ития к0мп4нии на 2024 г0д
    
    Це_лі прoекта:
    1. Увеliche_ние пp0даж на 20%
    2. l7м0дернізація oбoрудования
    3. Пoіп0внення штата на 5 с0трудників
    
    Тек5т с іыипичными 0шибк4ми ОСР:
    - ї zamененo на russian i
    - 0 zaмененo на нoль
    - l zamененo на unit
    """
    
    enhancer = TextEnhancer()
    
    # Анализируем качество
    analysis = enhancer.analyze_text_quality(test_text)
    print(f"📊 Оценка качества оригинального текста: {analysis['confidence_score']:.0f}%")
    print(f"🔍 Найдено украинских символов: {len(analysis['ukrainian_chars'])}")
    print(f"🔍 Найдено OCR ошибок: {len(analysis['ocr_errors'])}")
    
    if analysis['needs_enhancement']:
        print("🔧 Текст нуждается в улучшении...")
        
        enhanced_text = await enhancer.enhance_russian_text(test_text, "Тестовый документ")
        
        # Анализируем улучшенный текст
        enhanced_analysis = enhancer.analyze_text_quality(enhanced_text)
        
        print("\n📈 Результат улучшения:")
        print(f"Качество: {analysis['confidence_score']:.0f}% → {enhanced_analysis['confidence_score']:.0f}%")
        print(f"Улучшение: +{enhanced_analysis['confidence_score'] - analysis['confidence_score']:.0f}%")
        
        print("\n📝 Исходный текст:")
        print(test_text[:200] + "...")
        
        print("\n✨ Улучшенный текст:")
        print(enhanced_text[:200] + "...")
        
        # Получаем полную статистику
        stats = enhancer.get_enhancement_stats(test_text, enhanced_text)
        print(f"\n📊 Статистика улучшений:")
        print(f"- Исправлено украинских символов: {stats['ukrainian_chars_fixed']}")
        print(f"- Исправлено OCR ошибок: {stats['ocr_errors_fixed']}")
        
    else:
        print("✅ Текст не нуждается в улучшении")

def show_help():
    """Показывает справку"""
    print("🤖 Claude AI Manager для Telegram бота")
    print("=" * 50)
    print()
    print("Команды:")
    print("  status      - Показать текущий статус")
    print("  enable      - Включить Claude AI")
    print("  disable     - Отключить Claude AI")
    print("  test        - Тестировать улучшение текста")
    print("  help        - Показать эту справку")
    print()
    print("Примеры:")
    print("  python manage_claude.py status")
    print("  python manage_claude.py enable")
    print("  python manage_claude.py test")

async def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        show_status()
    elif command == 'enable':
        enable_claude()
    elif command == 'disable':
        disable_claude()
    elif command == 'test':
        await test_enhancement()
    elif command == 'help':
        show_help()
    else:
        print(f"❌ Неизвестная команда: {command}")
        print("Используйте 'help' для списка команд")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Управление Claude AI завершено")
    except Exception as e:
        print(f"❌ Ошибка: {e}") 