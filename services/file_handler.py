import os
import tempfile
import logging
from typing import Optional, Tuple
from pathlib import Path
from config.settings import MAX_FILE_SIZE

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def validate_file(self, file_path: str, file_size: int) -> Tuple[bool, str]:
        """Валидация загруженного файла"""
        
        # Проверка размера файла
        if file_size > MAX_FILE_SIZE:
            return False, f"Размер файла ({file_size // (1024*1024)} МБ) превышает максимально допустимый ({MAX_FILE_SIZE // (1024*1024)} МБ)"
        
        # Проверка расширения файла
        if not file_path.lower().endswith('.pdf'):
            return False, "Поддерживаются только PDF файлы"
        
        # Проверка, что файл действительно PDF (упрощенная проверка)
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                if not header.startswith(b'%PDF'):
                    return False, "Файл не является корректным PDF документом"
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return False, "Ошибка при чтении файла"
        
        return True, "OK"
    
    def get_temp_file_path(self, filename: str, suffix: str = "") -> str:
        """Получение пути для временного файла"""
        safe_filename = self.sanitize_filename(filename)
        if suffix:
            name, ext = os.path.splitext(safe_filename)
            safe_filename = f"{name}_{suffix}{ext}"
        
        return os.path.join(self.temp_dir, safe_filename)
    
    def sanitize_filename(self, filename: str) -> str:
        """Очистка имени файла от недопустимых символов"""
        # Удаляем или заменяем недопустимые символы
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Ограничиваем длину имени файла
        if len(filename) > 100:
            name, ext = os.path.splitext(filename)
            filename = name[:100-len(ext)] + ext
        
        return filename
    
    def save_telegram_file(self, file_content: bytes, filename: str) -> str:
        """Сохранение файла из Telegram во временную директорию"""
        temp_path = self.get_temp_file_path(filename, "input")
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(file_content)
            
            logger.info(f"File saved to {temp_path}")
            return temp_path
        
        except Exception as e:
            logger.error(f"Error saving file {filename}: {e}")
            raise
    
    def save_converted_file(self, file_content: bytes, original_filename: str) -> str:
        """Сохранение конвертированного файла"""
        # Меняем расширение на .xlsx
        name = os.path.splitext(original_filename)[0]
        xlsx_filename = f"{name}.xlsx"
        temp_path = self.get_temp_file_path(xlsx_filename, "output")
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(file_content)
            
            logger.info(f"Converted file saved to {temp_path}")
            return temp_path
        
        except Exception as e:
            logger.error(f"Error saving converted file: {e}")
            raise
    
    def cleanup_file(self, file_path: str):
        """Удаление временного файла"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {e}")
    
    def cleanup_files(self, *file_paths: str):
        """Удаление множественных временных файлов"""
        for file_path in file_paths:
            self.cleanup_file(file_path)
    
    def get_file_info(self, file_path: str) -> dict:
        """Получение информации о файле"""
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'exists': True
            }
        except Exception:
            return {
                'size': 0,
                'size_mb': 0,
                'exists': False
            }
    
    def is_pdf_valid(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Более детальная проверка PDF файла"""
        try:
            with open(file_path, 'rb') as f:
                # Проверяем заголовок PDF
                header = f.read(8)
                if not header.startswith(b'%PDF'):
                    return False, "Файл не является PDF документом"
                
                # Проверяем, что файл не поврежден (упрощенная проверка)
                f.seek(-1024, 2)  # Переходим к концу файла
                end_content = f.read()
                if b'%%EOF' not in end_content and b'startxref' not in end_content:
                    return False, "PDF файл может быть поврежден"
                
                return True, None
        
        except Exception as e:
            logger.error(f"Error validating PDF {file_path}: {e}")
            return False, f"Ошибка при проверке файла: {str(e)}" 