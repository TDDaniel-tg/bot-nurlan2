"""Клавиатуры и inline-кнопки для бота"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Главное меню команд
def get_main_menu() -> ReplyKeyboardMarkup:
    """Основное меню с командами"""
    keyboard = [
        [KeyboardButton("📤 Конвертировать файл"), KeyboardButton("📊 Статус")],
        [KeyboardButton("❓ Справка"), KeyboardButton("ℹ️ О боте")]
    ]
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие или отправьте PDF файл"
    )

# Inline-клавиатуры для различных действий
def get_start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для стартового сообщения"""
    keyboard = [
        [InlineKeyboardButton("📤 Начать конвертацию", callback_data="start_convert")],
        [InlineKeyboardButton("❓ Справка", callback_data="help"),
         InlineKeyboardButton("📊 Статус", callback_data="status")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_conversion_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для процесса конвертации"""
    keyboard = [
        [InlineKeyboardButton("📊 Проверить статус", callback_data="check_status")],
        [InlineKeyboardButton("🚫 Отменить", callback_data="cancel_conversion")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_file_confirmation_keyboard(file_name: str, file_size: float) -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения обработки файла"""
    keyboard = [
        [InlineKeyboardButton("✅ Конвертировать", callback_data="confirm_convert")],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_convert")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_status_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для проверки статуса"""
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить статус", callback_data="refresh_status")],
        [InlineKeyboardButton("🚫 Отменить задачу", callback_data="cancel_task")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_error_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для сообщений об ошибках"""
    keyboard = [
        [InlineKeyboardButton("🔄 Попробовать снова", callback_data="retry_convert")],
        [InlineKeyboardButton("❓ Справка", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_success_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура после успешной конвертации"""
    keyboard = [
        [InlineKeyboardButton("📤 Конвертировать еще файл", callback_data="convert_another")],
        [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_help_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для справки"""
    keyboard = [
        [InlineKeyboardButton("📤 Начать конвертацию", callback_data="start_convert")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Административная клавиатура (для будущего использования)"""
    keyboard = [
        [InlineKeyboardButton("📈 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("🔧 Настройки", callback_data="admin_settings")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Простая клавиатура отмены"""
    keyboard = [
        [InlineKeyboardButton("🚫 Отменить", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Функции для обработки callback данных
def parse_callback_data(data: str) -> dict:
    """Парсинг callback данных"""
    parts = data.split('_', 1)
    action = parts[0]
    params = parts[1] if len(parts) > 1 else None
    
    return {
        'action': action,
        'params': params
    }

# Удаление клавиатуры
def remove_keyboard() -> ReplyKeyboardMarkup:
    """Удаление reply клавиатуры"""
    return ReplyKeyboardMarkup([[]], resize_keyboard=True) 