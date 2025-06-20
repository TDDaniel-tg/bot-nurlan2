# 🤖 Управление Claude AI

Система улучшения качества OCR с помощью Claude AI для исправления ошибок распознавания русского текста.

## 🎯 Основные возможности

- ✅ **Исправление языковых ошибок** - автоматическое исправление украинских символов на русские
- 🔧 **Устранение OCR ошибок** - исправление типичных ошибок оптического распознавания  
- 📊 **Анализ качества** - оценка качества распознанного текста (0-100%)
- 📈 **Статистика улучшений** - подробная информация о внесенных исправлениях
- 🎨 **Улучшенная конвертация** - повышение качества PDF → XLSX конвертации

## 🔧 Управление через утилиту

```bash
# Проверить текущий статус
python manage_claude.py status

# Включить Claude AI  
python manage_claude.py enable

# Отключить Claude AI
python manage_claude.py disable

# Тестировать улучшение текста
python manage_claude.py test

# Показать справку
python manage_claude.py help
```

## ⚙️ Настройка

### Переменные окружения (.env)

```env
# Claude AI API Key (получить на https://console.anthropic.com/)
CLAUDE_API_KEY=sk-ant-api-key-here

# Модель Claude
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Управление Claude AI (true/false)
CLAUDE_MANUAL_ENABLED=true

# Настройки OCR для принудительного русского языка
CLOUDCONVERT_OCR_LANGUAGES=rus
CLOUDCONVERT_LOCALE=ru_RU
```

### Получение API ключа

1. Зарегистрируйтесь на https://console.anthropic.com/
2. Пополните баланс (минимум $5)
3. Создайте API ключ в разделе "API Keys"
4. Добавьте ключ в `.env` файл
5. Установите `CLAUDE_MANUAL_ENABLED=true`
6. Перезапустите бота

## 🚫 Решаемые проблемы OCR

### Языковые ошибки
Часто CloudConvert распознает русский текст как украинский:

- `ї` → `и` (украинская ї)
- `і` → `и` (украинская і)  
- `є` → `е` (украинская є)
- `ґ` → `г` (украинская ґ)
- `ў` → `у` (белорусская ў)

### Типичные ошибки OCR
- `О` ↔ `0` (буква О путается с цифрой 0)
- `I` ↔ `l` (заглавная I путается со строчной l)
- `rn` → `m` (сочетание rn распознается как m)
- Смешанные алфавиты в одном тексте
- Неправильная ориентация символов

## 📊 Работа в боте

### Без Claude AI
```
✅ Конвертация завершена успешно!
```

### С Claude AI (без улучшений)
```
✅ Конвертация завершена успешно!
✅ Качество проверено - улучшения не требуются
```

### С Claude AI (с улучшениями)
```
✅ Конвертация завершена успешно!
🤖 Текст улучшен с помощью Claude AI
📈 Качество: 65% → 95%
🔧 Исправлено украинских символов: 12
🔧 Исправлено OCR ошибок: 8
```

## 🧪 Тестирование

Команда `python manage_claude.py test` покажет:

```
🧪 Тестирование улучшения текста...
📊 Оценка качества оригинального текста: 45%
🔍 Найдено украинских символов: 8
🔍 Найдено OCR ошибок: 12

🔧 Текст нуждается в улучшении...

📈 Результат улучшения:
Качество: 45% → 95%
Улучшение: +50%

📝 Исходный текст:
Пр0ект пл4на pаз5ития к0мп4нії...

✨ Улучшенный текст:
Проект плана развития компании...

📊 Статистика улучшений:
- Исправлено украинских символов: 8
- Исправлено OCR ошибок: 12
```

## 💰 Стоимость использования

Claude AI работает по модели pay-per-use:

- **Входящие токены**: ~$0.003 за 1000 токенов
- **Исходящие токены**: ~$0.015 за 1000 токенов  
- **Средняя стоимость обработки**: $0.01-0.05 за документ
- **Рекомендация**: начните с $10-20 на балансе

## 🔒 Безопасность

- API ключ хранится в переменных окружения
- Claude AI отключен по умолчанию
- Требует ручного включения
- Весь текст обрабатывается через защищенные API
- Данные не сохраняются на серверах Anthropic

## 📝 Логирование

Все операции Claude AI записываются в логи:

```
INFO - Text enhancement stats: {'improvement': 50, 'ukrainian_chars_fixed': 8}
INFO - Successfully enhanced sheet 'Sheet1' with Claude AI
INFO - XLSX file enhancement completed successfully
```

## ❓ Решение проблем

### Claude AI не включается
- Проверьте наличие API ключа в `.env`
- Убедитесь что `CLAUDE_MANUAL_ENABLED=true`
- Перезапустите бота

### Ошибки API
- Проверьте баланс на console.anthropic.com
- Убедитесь что API ключ активен
- Проверьте подключение к интернету

### Плохое качество улучшений
- Используйте последнюю модель Claude
- Проверьте что файл содержит текст на русском
- Попробуйте команду `test` для диагностики 