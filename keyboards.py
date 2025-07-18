"""
Telegram inline keyboards module
Contains all keyboard layouts for the bot interface
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    """Get the main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("🎯 Начать тест", callback_data="start_quiz")],
        [InlineKeyboardButton("📊 Статистика", callback_data="statistics")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quiz_mode_keyboard():
    """Get the quiz mode selection keyboard."""
    keyboard = [
        [InlineKeyboardButton("🎓 Специальность (15)", callback_data="mode_specialty")],
        [InlineKeyboardButton("📚 Направление (30)", callback_data="mode_direction")],
        [InlineKeyboardButton("🔀 Микс режим", callback_data="mode_mixed")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quiz_control_keyboard():
    """Get the quiz control keyboard (shown during active quiz)."""
    keyboard = [
        [InlineKeyboardButton("⏹️ Остановить тест", callback_data="stop_quiz")],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_keyboard():
    """Get a simple back to main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_continue_or_stop_keyboard():
    """Get keyboard for continue or stop options."""
    keyboard = [
        [InlineKeyboardButton("➡️ Продолжить", callback_data="continue_quiz")],
        [InlineKeyboardButton("⏹️ Остановить тест", callback_data="stop_quiz")],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_game_over_keyboard():
    """Get keyboard for game over screen."""
    keyboard = [
        [InlineKeyboardButton("🎯 Играть заново", callback_data="start_quiz")],
        [InlineKeyboardButton("📊 Статистика", callback_data="statistics")],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)
