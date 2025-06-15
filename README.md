# 🤖 Telegram PDF to XLSX Converter Bot

Telegram бот для конвертации PDF файлов в XLSX с улучшенным качеством OCR и автоматическим исправлением украинского текста на русский.

## ✨ Основные возможности

- 📄 **Конвертация PDF → XLSX** с высоким качеством OCR
- 🇺🇦➡️🇷🇺 **Автоматическое исправление украинского текста** на русский
- 🤖 **Улучшение качества с помощью Claude AI** (опционально)
- 📊 **Многоуровневая система обработки** для максимального качества
- 🔒 **Безопасность и приватность** - все данные обрабатываются локально
- 📈 **Статистика и мониторинг** операций

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd bot_nurlan2
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Скопируйте файл `env.example` в `.env` и заполните необходимые данные:

```bash
cp env.example .env
```

Отредактируйте `.env` файл:
```env
# Обязательные настройки
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
CLOUDCONVERT_API_KEY=your_cloudconvert_api_key_here

# Языковые настройки (для принудительного русского OCR)
CLOUDCONVERT_OCR_LANGUAGES=rus
CLOUDCONVERT_LOCALE=ru_RU

# Опциональные настройки Claude AI (для улучшения качества)
CLAUDE_API_KEY=your_claude_api_key_here
CLAUDE_MANUAL_ENABLED=true

# Дополнительные настройки
MAX_FILE_SIZE=20971520
LOG_LEVEL=INFO
```

### 4. Получение API ключей

#### Telegram Bot Token
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env`

#### CloudConvert API Key
1. Зарегистрируйтесь на [CloudConvert](https://cloudconvert.com/api/v2)
2. Получите API ключ в панели управления
3. Скопируйте ключ в `.env`

#### Claude AI API Key (опционально)
1. Зарегистрируйтесь на [Anthropic Console](https://console.anthropic.com/)
2. Получите API ключ
3. Скопируйте ключ в `.env`

### 5. Запуск бота
```bash
python main.py
```

## 🐳 Docker развертывание

### Сборка и запуск
```bash
docker-compose up -d
```

### Остановка
```bash
docker-compose down
```

## 📋 Требования

- Python 3.9+
- Telegram Bot Token
- CloudConvert API Key
- Claude AI API Key (опционально, для улучшения качества)

## 🔧 Конфигурация

### Языковые настройки
Бот настроен для принудительного распознавания русского текста:
- `CLOUDCONVERT_OCR_LANGUAGES=rus` - только русский язык
- `CLOUDCONVERT_LOCALE=ru_RU` - русская локаль

### Система исправления украинского текста
Бот автоматически исправляет украинский текст на русский через:
1. **Принудительную замену** на уровне CloudConvert
2. **Постобработку** с 150+ правилами замены
3. **Claude AI** для дополнительного улучшения качества

### Лимиты
- Максимальный размер файла: 20 МБ
- Лимит запросов: 1 файл в минуту на пользователя
- Таймаут конвертации: 5 минут

## 📊 Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/convert` - Инструкции по конвертации
- `/status` - Проверить статус обработки

## 🛠️ Управление

### Проверка кредитов CloudConvert
```bash
python check_credits.py
```

### Управление Claude AI
```bash
python manage_claude.py
```

### Тестирование интеграций
```bash
python test_claude_integration.py
python test_language_settings.py
```

## 📁 Структура проекта

```
bot_nurlan2/
├── bot/                    # Telegram bot логика
│   ├── handlers.py        # Обработчики команд и файлов
│   ├── keyboards.py       # Клавиатуры (не в репозитории)
│   └── messages.py        # Сообщения бота
├── config/                # Конфигурация
│   └── settings.py        # Настройки приложения
├── services/              # Сервисы
│   ├── cloudconvert.py    # CloudConvert API
│   ├── claude_service.py  # Claude AI интеграция
│   ├── database.py        # База данных
│   ├── file_handler.py    # Обработка файлов
│   └── text_enhancer.py   # Улучшение текста
├── utils/                 # Утилиты
│   └── admin.py          # Административные функции
├── .env.example          # Пример переменных окружения
├── requirements.txt      # Python зависимости
├── Dockerfile           # Docker конфигурация
└── docker-compose.yml   # Docker Compose
```

## 🔒 Безопасность

### Исключенные из репозитория файлы
- `.env` - переменные окружения с секретами
- `bot.db` - база данных
- `*.log` - лог файлы
- `__pycache__/` - кэш Python
- Все файлы с токенами и ключами

### Рекомендации
- Никогда не коммитьте файл `.env`
- Используйте сильные API ключи
- Регулярно ротируйте токены
- Мониторьте использование API

## 📈 Мониторинг

Бот ведет подробные логи всех операций:
- Успешные конвертации
- Ошибки обработки
- Статистика пользователей
- Использование API

## 🆘 Поддержка

Если возникли проблемы:
1. Проверьте файл `TROUBLESHOOTING.md`
2. Убедитесь, что все API ключи корректны
3. Проверьте логи в `bot_dev.log`
4. Проверьте кредиты CloudConvert

## 📄 Лицензия

Этот проект предназначен для личного использования.

---

**Примечание**: Для работы бота требуются действующие API ключи CloudConvert и Telegram. Claude AI опционален, но рекомендуется для лучшего качества обработки текста. 