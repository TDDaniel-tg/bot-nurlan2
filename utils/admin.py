#!/usr/bin/env python3
"""
Административные утилиты для управления ботом
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# Добавляем корневую директорию в Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from services.database import Database

class AdminUtils:
    def __init__(self, db_path: str = "bot.db"):
        self.db = Database(db_path)
    
    def show_stats(self):
        """Показать общую статистику"""
        stats = self.db.get_stats()
        
        print("📊 Статистика бота")
        print("=" * 40)
        print(f"📈 Всего операций: {stats['total_operations']}")
        print(f"✅ Успешных: {stats['successful_operations']}")
        print(f"❌ С ошибками: {stats['error_operations']}")
        print(f"👥 Уникальных пользователей: {stats['unique_users']}")
        print(f"📊 Успешность: {stats['success_rate']:.1f}%")
    
    def show_recent_operations(self, limit: int = 10):
        """Показать последние операции"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, username, operation, status, file_name, 
                       created_at, error_message
                FROM operations_log 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            operations = cursor.fetchall()
        
        print(f"\n📋 Последние {limit} операций")
        print("=" * 80)
        
        for op in operations:
            user_id, username, operation, status, file_name, created_at, error = op
            status_emoji = "✅" if status == "completed" else "❌" if status == "error" else "🔄"
            
            print(f"{status_emoji} {created_at} | User: {user_id} ({username or 'N/A'})")
            print(f"   Operation: {operation} | File: {file_name or 'N/A'}")
            if error:
                print(f"   Error: {error}")
            print()
    
    def show_active_tasks(self):
        """Показать активные задачи"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, job_id, file_name, created_at
                FROM active_tasks
                ORDER BY created_at DESC
            ''')
            
            tasks = cursor.fetchall()
        
        print(f"\n🔄 Активные задачи ({len(tasks)})")
        print("=" * 50)
        
        if not tasks:
            print("Нет активных задач")
            return
        
        for task in tasks:
            user_id, job_id, file_name, created_at = task
            print(f"👤 User: {user_id} | Job: {job_id}")
            print(f"📄 File: {file_name}")
            print(f"⏰ Started: {created_at}")
            print()
    
    def clean_old_logs(self, days: int = 30):
        """Очистка старых логов"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Подсчитываем количество записей для удаления
            cursor.execute('''
                SELECT COUNT(*) FROM operations_log 
                WHERE created_at < ?
            ''', (cutoff_date.isoformat(),))
            
            count = cursor.fetchone()[0]
            
            if count == 0:
                print(f"Нет записей старше {days} дней для удаления")
                return
            
            # Удаляем старые записи
            cursor.execute('''
                DELETE FROM operations_log 
                WHERE created_at < ?
            ''', (cutoff_date.isoformat(),))
            
            conn.commit()
            
            print(f"🗑️ Удалено {count} записей старше {days} дней")
    
    def clear_active_tasks(self):
        """Очистка всех активных задач"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM active_tasks')
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("Нет активных задач для очистки")
                return
            
            cursor.execute('DELETE FROM active_tasks')
            conn.commit()
            
            print(f"🗑️ Очищено {count} активных задач")
    
    def show_top_users(self, limit: int = 10):
        """Показать топ пользователей по активности"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, username, COUNT(*) as operations,
                       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as successful,
                       MAX(created_at) as last_activity
                FROM operations_log 
                GROUP BY user_id 
                ORDER BY operations DESC 
                LIMIT ?
            ''', (limit,))
            
            users = cursor.fetchall()
        
        print(f"\n👥 Топ {limit} пользователей")
        print("=" * 70)
        
        for user in users:
            user_id, username, operations, successful, last_activity = user
            success_rate = (successful / operations * 100) if operations > 0 else 0
            
            print(f"👤 {user_id} ({username or 'N/A'})")
            print(f"   📊 Операций: {operations} | Успешных: {successful} ({success_rate:.1f}%)")
            print(f"   ⏰ Последняя активность: {last_activity}")
            print()

def main():
    """Главная функция CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Административные утилиты для PDF to Excel Bot")
    parser.add_argument('--db', default='bot.db', help='Путь к базе данных')
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда stats
    subparsers.add_parser('stats', help='Показать общую статистику')
    
    # Команда recent
    recent_parser = subparsers.add_parser('recent', help='Показать последние операции')
    recent_parser.add_argument('--limit', type=int, default=10, help='Количество записей')
    
    # Команда active
    subparsers.add_parser('active', help='Показать активные задачи')
    
    # Команда cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Очистка данных')
    cleanup_parser.add_argument('--logs', type=int, help='Удалить логи старше N дней')
    cleanup_parser.add_argument('--tasks', action='store_true', help='Очистить активные задачи')
    
    # Команда users
    users_parser = subparsers.add_parser('users', help='Показать топ пользователей')
    users_parser.add_argument('--limit', type=int, default=10, help='Количество пользователей')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    admin = AdminUtils(args.db)
    
    try:
        if args.command == 'stats':
            admin.show_stats()
        
        elif args.command == 'recent':
            admin.show_recent_operations(args.limit)
        
        elif args.command == 'active':
            admin.show_active_tasks()
        
        elif args.command == 'cleanup':
            if args.logs:
                admin.clean_old_logs(args.logs)
            if args.tasks:
                admin.clear_active_tasks()
            if not args.logs and not args.tasks:
                print("Укажите --logs или --tasks для очистки")
        
        elif args.command == 'users':
            admin.show_top_users(args.limit)
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 