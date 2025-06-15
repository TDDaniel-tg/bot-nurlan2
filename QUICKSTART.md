# 🚀 Быстрый старт бота

## 📋 Что нужно для работы

1. **Telegram Bot Token** - создайте через @BotFather
2. **CloudConvert API Key** - получите на cloudconvert.com
3. **Claude AI API Key** *(опционально)* - для улучшения качества OCR

## ⚡ Быстрая установка

### 1. Клонирование и настройка
```bash
git clone <repository-url>
cd bot_nurlan2
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
Скопируйте `env.example` в `.env` и заполните:

```env
# Обязательные настройки
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
CLOUDCONVERT_API_KEY=your_cloudconvert_api_key

# Для качественного русского OCR
CLOUDCONVERT_OCR_LANGUAGES=rus
CLOUDCONVERT_LOCALE=ru_RU

# Для улучшения качества (опционально)
CLAUDE_API_KEY=sk-ant-your-claude-key
CLAUDE_MANUAL_ENABLED=true
```

### 3. Запуск бота
```bash
python main.py
```

## 🇷🇺 Проблема с русским текстом?

**Симптомы:** Получаете украинские символы вместо русских?

**Решение:** 

1. **Убедитесь в настройках OCR:**
   ```env
   CLOUDCONVERT_OCR_LANGUAGES=rus
   CLOUDCONVERT_LOCALE=ru_RU
   ```

2. **Включите Claude AI для исправлений:**
   ```bash
   python manage_claude.py enable
   python manage_claude.py test  # Проверить работу
   ```

3. **Перезапустите бота:**
   ```bash
   python main.py
   ```

## 🧪 Тестирование

### Базовая конвертация
1. Отправьте PDF файл боту
2. Используйте команду `/convert`
3. Получите XLSX файл

### С улучшением качества
```bash
# Проверьте статус Claude AI
python manage_claude.py status

# Протестируйте улучшения
python manage_claude.py test

# Включите если нужно
python manage_claude.py enable
```

## 📊 Ожидаемый результат

### Без Claude AI
```
✅ Конвертация завершена успешно!
```

### С Claude AI
```
✅ Конвертация завершена успешно!
🤖 Текст улучшен с помощью Claude AI  
📈 Качество: 65% → 95%
🔧 Исправлено украинских символов: 12
🔧 Исправлено OCR ошибок: 8
```

## 🔧 Команды бота

- `/start` - Приветствие и главное меню
- `/help` - Справка по использованию  
- `/convert` - Начать конвертацию
- `/status` - Статус текущих задач

## 🐳 Docker запуск

```bash
# Настройте .env файл
cp env.example .env
# Отредактируйте .env

# Запустите контейнер
docker-compose up -d

# Проверьте логи
docker-compose logs -f
```

## 🚨 Решение проблем

### Бот не отвечает
- Проверьте `TELEGRAM_BOT_TOKEN` в `.env`
- Убедитесь что бот запущен: `python main.py`

### Ошибки конвертации
- Проверьте `CLOUDCONVERT_API_KEY` в `.env`
- Убедитесь что есть кредиты на CloudConvert
- Проверьте размер файла (максимум 20 МБ)

### Плохое качество OCR
- Установите `CLOUDCONVERT_OCR_LANGUAGES=rus`
- Включите Claude AI: `python manage_claude.py enable`
- Проверьте API ключ Claude в `.env`

### Claude AI не работает
- Добавьте баланс на console.anthropic.com (минимум $5)
- Проверьте API ключ: `python manage_claude.py status`
- Убедитесь: `CLAUDE_MANUAL_ENABLED=true`

## 📝 Логи и мониторинг

```bash
# Логи в реальном времени
python main.py

# В Docker
docker-compose logs -f bot

# Проверка базы данных
python -c "from services.database import DatabaseService; db = DatabaseService(); print(db.get_stats())"
```

## 🔗 Полезные ссылки

- **CloudConvert API**: https://cloudconvert.com/api/v2
- **Claude AI Console**: https://console.anthropic.com/
- **Telegram Bot API**: https://core.telegram.org/bots
- **Документация проекта**: README.md

## 💰 Примерная стоимость

- **CloudConvert**: $0.01-0.02 за конвертацию  
- **Claude AI**: $0.01-0.05 за улучшение
- **Общая стоимость**: $0.02-0.07 за документ

**Рекомендация**: начните с $10-20 на каждом сервисе 