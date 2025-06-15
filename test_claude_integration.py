#!/usr/bin/env python3
"""
Тест интеграции с Claude AI
"""

import asyncio
import os
from dotenv import load_dotenv
from services.claude_service import ClaudeService

load_dotenv()

async def test_claude_service():
    """Тестирование Claude сервиса"""
    print("🤖 Тестирование Claude AI сервиса...")
    
    # Проверяем наличие API ключа
    if not os.getenv('CLAUDE_API_KEY'):
        print("❌ CLAUDE_API_KEY не найден в переменных окружения")
        return
    
    try:
        claude = ClaudeService()
        print("✅ Claude сервис инициализирован")
        
        # Тестовые данные (имитация PDF и XLSX)
        test_pdf_data = b"PDF test data content"
        test_xlsx_data = b"XLSX test data content"
        
        # Тест анализа качества
        print("📊 Тестирование анализа качества...")
        success, report = await claude.analyze_conversion_quality(
            test_pdf_data, test_xlsx_data
        )
        
        if success:
            print(f"✅ Анализ качества успешен:\n{report}")
        else:
            print(f"❌ Ошибка анализа: {report}")
            
        # Тест "улучшения" файла (на самом деле анализа)
        print("🔄 Тестирование анализа файла...")
        enhanced_data = await claude.enhance_xlsx_file(
            test_pdf_data, test_xlsx_data, "test.pdf"
        )
        
        if enhanced_data:
            print("✅ Анализ файла завершен успешно")
        else:
            print("❌ Ошибка анализа файла")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    asyncio.run(test_claude_service()) 