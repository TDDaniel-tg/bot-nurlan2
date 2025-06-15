import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "bot.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация базы данных"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Таблица для логирования операций
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operations_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    operation TEXT NOT NULL,
                    status TEXT NOT NULL,
                    file_name TEXT,
                    file_size INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    error_message TEXT
                )
            ''')
            
            # Таблица для отслеживания лимитов пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_limits (
                    user_id INTEGER PRIMARY KEY,
                    last_request TIMESTAMP,
                    request_count INTEGER DEFAULT 0
                )
            ''')
            
            # Таблица для активных задач
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS active_tasks (
                    user_id INTEGER PRIMARY KEY,
                    job_id TEXT,
                    file_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для работы с соединением"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def log_operation(self, user_id: int, username: str, operation: str, 
                     status: str, file_name: str = None, file_size: int = None,
                     error_message: str = None) -> int:
        """Логирование операции"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO operations_log 
                (user_id, username, operation, status, file_name, file_size, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, operation, status, file_name, file_size, error_message))
            conn.commit()
            return cursor.lastrowid
    
    def update_operation_status(self, operation_id: int, status: str, error_message: str = None):
        """Обновление статуса операции"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE operations_log 
                SET status = ?, completed_at = CURRENT_TIMESTAMP, error_message = ?
                WHERE id = ?
            ''', (status, error_message, operation_id))
            conn.commit()
    
    def check_user_rate_limit(self, user_id: int) -> bool:
        """Проверка лимита запросов пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Получаем последний запрос пользователя
            cursor.execute('''
                SELECT last_request FROM user_limits WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            now = datetime.now()
            
            if result:
                last_request = datetime.fromisoformat(result['last_request'])
                if now - last_request < timedelta(minutes=1):
                    return False
            
            # Обновляем время последнего запроса
            cursor.execute('''
                INSERT OR REPLACE INTO user_limits (user_id, last_request, request_count)
                VALUES (?, ?, COALESCE((SELECT request_count + 1 FROM user_limits WHERE user_id = ?), 1))
            ''', (user_id, now.isoformat(), user_id))
            
            conn.commit()
            return True
    
    def save_active_task(self, user_id: int, job_id: str, file_name: str):
        """Сохранение активной задачи"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO active_tasks (user_id, job_id, file_name)
                VALUES (?, ?, ?)
            ''', (user_id, job_id, file_name))
            conn.commit()
    
    def get_active_task(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение активной задачи пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM active_tasks WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def remove_active_task(self, user_id: int):
        """Удаление активной задачи"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM active_tasks WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Общее количество операций
            cursor.execute('SELECT COUNT(*) as total FROM operations_log')
            total_operations = cursor.fetchone()['total']
            
            # Успешные операции
            cursor.execute('SELECT COUNT(*) as success FROM operations_log WHERE status = "completed"')
            successful_operations = cursor.fetchone()['success']
            
            # Операции с ошибками
            cursor.execute('SELECT COUNT(*) as errors FROM operations_log WHERE status = "error"')
            error_operations = cursor.fetchone()['errors']
            
            # Уникальные пользователи
            cursor.execute('SELECT COUNT(DISTINCT user_id) as users FROM operations_log')
            unique_users = cursor.fetchone()['users']
            
            return {
                'total_operations': total_operations,
                'successful_operations': successful_operations,
                'error_operations': error_operations,
                'unique_users': unique_users,
                'success_rate': (successful_operations / total_operations * 100) if total_operations > 0 else 0
            } 