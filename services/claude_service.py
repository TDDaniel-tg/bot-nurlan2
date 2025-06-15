import asyncio
import logging
import base64
from typing import Optional, Tuple
from anthropic import AsyncAnthropic
from config.settings import CLAUDE_API_KEY, CLAUDE_MODEL

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=CLAUDE_API_KEY)
        self.model = CLAUDE_MODEL
    
    async def enhance_xlsx_file(self, pdf_data: bytes, xlsx_data: bytes, original_filename: str) -> Optional[bytes]:
        """
        Улучшение XLSX файла с помощью Claude AI
        
        Args:
            pdf_data: Данные исходного PDF файла
            xlsx_data: Данные XLSX файла от CloudConvert
            original_filename: Имя исходного файла
        
        Returns:
            Улучшенные данные XLSX файла или None при ошибке
        """
        try:
            # Ограничиваем размер файлов для анализа (первые 50KB каждого)
            pdf_sample = pdf_data[:51200] if len(pdf_data) > 51200 else pdf_data
            xlsx_sample = xlsx_data[:51200] if len(xlsx_data) > 51200 else xlsx_data
            
            # Кодируем образцы в base64
            pdf_base64 = base64.b64encode(pdf_sample).decode('utf-8')
            xlsx_base64 = base64.b64encode(xlsx_sample).decode('utf-8')
            
            # Создаем системное сообщение
            system_message = """Ты - эксперт по анализу качества конвертации PDF в XLSX. 

Твоя задача:
1. Проанализировать структуру и содержание PDF файла
2. Проанализировать качество XLSX конвертации
3. Дать рекомендации по улучшению

НЕ ПЫТАЙСЯ создавать новый XLSX файл. Только анализируй качество конвертации и предложи текстовые рекомендации для улучшения."""

            # Создаем сообщение пользователя  
            user_message = f"""Проанализируй качество конвертации PDF в XLSX:

PDF образец (base64): {pdf_base64}

XLSX образец (base64): {xlsx_base64}

Имя файла: {original_filename}

Проанализируй:
1. Правильность извлечения данных
2. Сохранность структуры таблиц 
3. Точность форматирования
4. Потенциальные проблемы

Дай краткие рекомендации по улучшению качества."""

            # Отправляем запрос к Claude
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_message,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            
            # Получаем анализ, но возвращаем оригинальный файл
            # (так как Claude не может создавать настоящие XLSX файлы)
            if response.content and len(response.content) > 0:
                analysis = response.content[0].text.strip()
                logger.info(f"Claude analysis for {original_filename}: {analysis[:200]}...")
                
            # Возвращаем оригинальный XLSX файл
            # В реальности Claude не может создать валидный XLSX файл
            logger.info(f"Returning original XLSX file for {original_filename}")
            return xlsx_data
        
        except Exception as e:
            logger.error(f"Error analyzing XLSX file with Claude: {e}")
            # Возвращаем оригинальный файл при ошибке
            return xlsx_data
    
    async def analyze_conversion_quality(self, pdf_data: bytes, xlsx_data: bytes) -> Tuple[bool, str]:
        """
        Анализ качества конвертации
        
        Args:
            pdf_data: Данные PDF файла
            xlsx_data: Данные XLSX файла
        
        Returns:
            Tuple[bool, str]: (success, quality_report)
        """
        try:
            # Ограничиваем размер для анализа
            pdf_sample = pdf_data[:25600] if len(pdf_data) > 25600 else pdf_data
            xlsx_sample = xlsx_data[:25600] if len(xlsx_data) > 25600 else xlsx_data
            
            pdf_base64 = base64.b64encode(pdf_sample).decode('utf-8')
            xlsx_base64 = base64.b64encode(xlsx_sample).decode('utf-8')
            
            system_message = """Ты - эксперт по анализу качества конвертации документов. 
Проанализируй образцы PDF и XLSX файлов и дай оценку качества конвертации.

Дай краткий отчет (максимум 150 слов) о:
1. Общей оценке качества (отлично/хорошо/удовлетворительно/плохо)  
2. Основных проблемах (если есть)
3. Рекомендациях по улучшению"""

            user_message = f"""Оцени качество конвертации PDF в XLSX:

PDF образец: {pdf_base64}
XLSX образец: {xlsx_base64}

Дай краткую оценку качества конвертации."""

            response = await self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=system_message,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            
            if response.content and len(response.content) > 0:
                quality_report = response.content[0].text.strip()
                logger.info("Successfully analyzed conversion quality")
                return True, quality_report
            else:
                return False, "Не удалось проанализировать качество конвертации"
        
        except Exception as e:
            logger.error(f"Error analyzing conversion quality: {e}")
            return False, f"Ошибка анализа: {str(e)}" 