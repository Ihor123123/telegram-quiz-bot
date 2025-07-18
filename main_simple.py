#!/usr/bin/env python3
"""
Simple Telegram Quiz Bot without database - Railway version
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from quiz_data import get_random_question

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    keyboard = [
        [InlineKeyboardButton("🎯 Начать викторину", callback_data='start_quiz')],
        [InlineKeyboardButton("📖 Помощь", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🎓 *Добро пожаловать в Quiz Bot!*\n\n"
        "Это бот для проверки знаний экзаменационных вопросов.\n\n"
        "Выберите действие:"
    )
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = (
        "📚 *Помощь по Quiz Bot*\n\n"
        "🎯 *Как играть:*\n"
        "• Нажмите 'Начать викторину'\n"
        "• Вам будет показан вопрос\n"
        "• Введите номер вопроса\n"
        "• Получите результат\n\n"
        "🔢 *Доступные вопросы:*\n"
        "• Specialty: вопросы 1-15\n"
        "• Direction: вопросы 1-30\n\n"
        "💡 *Команды:*\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку"
    )
    
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_quiz':
        await start_quiz(query, context)
    elif query.data == 'help':
        await show_help(query, context)
    elif query.data == 'main_menu':
        await show_main_menu(query, context)
    elif query.data == 'new_question':
        await start_quiz(query, context)

async def start_quiz(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a new quiz question"""
    question_data = get_random_question()
    
    question_text = f"**{question_data['question']}**"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Следующий вопрос", callback_data='new_question')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Store question data in context for checking answer
    context.user_data['current_question'] = question_data
    
    await query.edit_message_text(
        question_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_help(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help information"""
    help_text = (
        "📚 *Помощь по Quiz Bot*\n\n"
        "🎯 *Как играть:*\n"
        "• Нажмите 'Начать викторину'\n"
        "• Вам будет показан вопрос\n"
        "• Введите номер вопроса\n"
        "• Получите результат\n\n"
        "🔢 *Доступные вопросы:*\n"
        "• Specialty: вопросы 1-15\n"
        "• Direction: вопросы 1-30\n\n"
        "💡 *Команды:*\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку"
    )
    
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_main_menu(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main menu"""
    keyboard = [
        [InlineKeyboardButton("🎯 Начать викторину", callback_data='start_quiz')],
        [InlineKeyboardButton("📖 Помощь", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🎓 *Добро пожаловать в Quiz Bot!*\n\n"
        "Это бот для проверки знаний экзаменационных вопросов.\n\n"
        "Выберите действие:"
    )
    
    await query.edit_message_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages (answers)"""
    if 'current_question' not in context.user_data:
        await update.message.reply_text("Сначала начните викторину командой /start")
        return
    
    try:
        user_answer = int(update.message.text.strip())
        question_data = context.user_data['current_question']
        correct_answer = question_data['answer']
        
        if user_answer == correct_answer:
            result_text = f"✅ *Правильно!*\n\nВопрос: {question_data['question']}\nПравильный ответ: {correct_answer}"
            emoji = "🎉"
        else:
            result_text = f"❌ *Неправильно*\n\nВопрос: {question_data['question']}\nВаш ответ: {user_answer}\nПравильный ответ: {correct_answer}"
            emoji = "😔"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Следующий вопрос", callback_data='new_question')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            result_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число (номер вопроса)")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    # Get bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN environment variable is not set!")
        print("Please set your bot token in Railway environment variables.")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()