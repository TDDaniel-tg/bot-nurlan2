import asyncio
import logging
import signal
import sys
import os
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config.settings import TELEGRAM_BOT_TOKEN, LOG_LEVEL
from bot.handlers import BotHandlers
from services.database import Database
from health_server import HealthServer

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

def main():
    """Главная функция для запуска бота"""
    try:
        # Запуск health server для Railway
        port = int(os.getenv('PORT', 8080))
        health_server = HealthServer(port)
        health_server.start_server()
        
        # Инициализация базы данных
        logger.info("Initializing database...")
        db = Database()
        
        # Создание приложения
        logger.info("Creating bot application...")
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Инициализация обработчиков
        handlers = BotHandlers()
        
        # Регистрация обработчиков команд
        application.add_handler(CommandHandler("start", handlers.start_command))
        application.add_handler(CommandHandler("help", handlers.help_command))
        application.add_handler(CommandHandler("convert", handlers.convert_command))
        application.add_handler(CommandHandler("status", handlers.status_command))
        
        # Обработчик документов
        application.add_handler(MessageHandler(
            filters.Document.ALL, 
            handlers.handle_document
        ))
        
        # Обработчик callback кнопок
        application.add_handler(CallbackQueryHandler(handlers.handle_callback_query))
        
        # Обработчик неизвестных команд
        application.add_handler(MessageHandler(
            filters.COMMAND, 
            handlers.handle_unknown_command
        ))
        
        logger.info("Bot handlers registered successfully")
        
        # Запуск бота
        logger.info("Starting bot...")
        logger.info("Bot is running! Press Ctrl+C to stop.")
        
        # Запуск polling
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 