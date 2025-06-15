import os
from dotenv import load_dotenv

load_dotenv()

# Telegram настройки
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# CloudConvert настройки
CLOUDCONVERT_API_KEY = os.getenv('CLOUDCONVERT_API_KEY')
CLOUDCONVERT_BASE_URL = 'https://api.cloudconvert.com/v2'

# Языковые настройки CloudConvert
CLOUDCONVERT_OCR_LANGUAGES = os.getenv('CLOUDCONVERT_OCR_LANGUAGES', 'rus,eng').split(',')
CLOUDCONVERT_LOCALE = os.getenv('CLOUDCONVERT_LOCALE', 'ru_RU')

# Claude AI настройки
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

# Автоматическое включение Claude AI если есть API ключ (рекомендуется для лучшего качества)
CLAUDE_MANUAL_ENABLED = os.getenv('CLAUDE_MANUAL_ENABLED', 'true').lower() == 'true'  # По умолчанию включен

# База данных
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')

# Лимиты файлов
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 20971520))  # 20MB в байтах
# MAX_PAGES - убрано ограничение на количество страниц

# Логирование
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Лимиты пользователей
USER_REQUEST_LIMIT = 1  # файл в минуту на пользователя

# Таймауты
CONVERSION_TIMEOUT = 300  # 5 минут
API_TIMEOUT = 30  # 30 секунд

# Сообщения об ошибках
ERROR_MESSAGES = {
    'invalid_format': '❌ Поддерживаются только PDF файлы',
    'file_too_large': f'❌ Размер файла не должен превышать {MAX_FILE_SIZE // (1024*1024)} МБ',
    'api_error': '❌ Ошибка сервиса конвертации. Попробуйте позже',
    'conversion_failed': '❌ Не удалось конвертировать файл',
    'timeout': '❌ Превышено время ожидания обработки',
    'rate_limit': '❌ Слишком частые запросы. Попробуйте через минуту',
    'no_token': '❌ Не настроен токен бота',
    'no_api_key': '❌ Не настроен API ключ CloudConvert'
}

# Проверка обязательных переменных
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен")

if not CLOUDCONVERT_API_KEY:
    raise ValueError("CLOUDCONVERT_API_KEY не установлен")

# Claude AI опционален и управляется вручную
CLAUDE_ENABLED = bool(CLAUDE_API_KEY) and CLAUDE_MANUAL_ENABLED
if CLAUDE_API_KEY and CLAUDE_MANUAL_ENABLED:
    print("✅ Claude AI включен")
elif CLAUDE_API_KEY and not CLAUDE_MANUAL_ENABLED:
    print("⚠️ Claude AI доступен, но отключен вручную")
else:
    print("⚠️ Claude AI недоступен (нет API ключа)") 