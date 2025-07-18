"""
Telegram bot handlers module
Contains all message and callback handlers for the quiz bot
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database import (
    get_user_stats, update_user_info, update_user_quiz_mode,
    record_correct_answer, record_incorrect_answer, clear_quiz_mode,
    reset_lives, get_lives_display
)
from quiz_data import (
    get_random_question, validate_answer, get_source_display_name,
    get_max_question_number
)
from keyboards import (
    get_main_menu_keyboard, get_quiz_mode_keyboard, get_quiz_control_keyboard,
    get_back_to_main_keyboard, get_continue_or_stop_keyboard, get_game_over_keyboard
)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user = update.effective_user
    
    # Update user info in database
    update_user_info(user.id, user.username, user.first_name)
    
    welcome_text = f"""
🎓 <b>Добро пожаловать в Quiz Bot!</b>

Привет, {user.first_name}! 👋

Этот бот поможет тебе проверить знание номеров экзаменационных вопросов.

<b>Как это работает:</b>
• Выбираешь режим тестирования
• Бот показывает вопрос
• Ты отвечаешь номером вопроса
• Следишь за своими стриками и рекордами

<b>Режимы тестирования:</b>
🎓 <b>Специальность</b> - 15 вопросов
📚 <b>Направление</b> - 30 вопросов  
🔀 <b>Микс</b> - случайные вопросы из обеих категорий

Удачи в подготовке! 🍀
"""
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    help_text = """
📖 <b>Помощь по использованию бота</b>

<b>Основные команды:</b>
/start - Запустить бота
/help - Показать эту справку

<b>Режимы тестирования:</b>
🎓 <b>Специальность (15)</b> - Вопросы 1-15 по специальности
📚 <b>Направление (30)</b> - Вопросы 1-30 по направлению
🔀 <b>Микс режим</b> - Случайное сочетание вопросов

<b>Как отвечать:</b>
• Бот показывает текст вопроса
• Ты пишешь номер этого вопроса (число от 1 до 15/30)
• При правильном ответе тест продолжается автоматически
• При неправильном - бот ждет правильный ответ

<b>Статистика:</b>
📊 Текущий стрик - количество правильных ответов подряд
🏆 Рекорд - максимальный стрик за все время
📈 Общая статистика ответов

<b>Управление:</b>
⏹️ Остановить тест - выйти из режима тестирования
⬅️ Назад - вернуться в предыдущее меню
"""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            help_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_to_main_keyboard()
        )
    else:
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard()
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "start_quiz":
        await show_quiz_mode_selection(query)
    elif data == "statistics":
        await show_statistics(query)
    elif data == "help":
        await help_command(update, context)
    elif data == "back_to_main":
        await show_main_menu(query)
    elif data.startswith("mode_"):
        mode = data.replace("mode_", "")
        await start_quiz_mode(query, mode)
    elif data == "stop_quiz":
        await stop_quiz(query)

    else:
        await query.edit_message_text("❌ Неизвестная команда")

async def show_main_menu(query):
    """Show the main menu."""
    user = query.from_user
    stats = get_user_stats(user.id)
    
    menu_text = f"""
🎓 <b>Quiz Bot - Главное меню</b>

Привет, {user.first_name}! 👋

📊 <b>Твоя статистика:</b>
🔥 Текущий стрик: <b>{stats['current_streak']}</b>
🏆 Лучший результат: <b>{stats['best_streak']}</b>
📈 Правильных ответов: <b>{stats['correct_answers']}</b>/{stats['total_questions']}

Выбери действие:
"""
    
    await query.edit_message_text(
        menu_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard()
    )

async def show_quiz_mode_selection(query):
    """Show quiz mode selection."""
    mode_text = """
🎯 <b>Выбор режима тестирования</b>

Выбери режим для проверки знаний:

🎓 <b>Специальность (15)</b>
   Вопросы 1-15 по специальности

📚 <b>Направление (30)</b>
   Вопросы 1-30 по направлению

🔀 <b>Микс режим</b>
   Случайные вопросы из обеих категорий
   (с указанием источника)
"""
    
    await query.edit_message_text(
        mode_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_quiz_mode_keyboard()
    )

async def show_statistics(query):
    """Show user statistics."""
    user_id = query.from_user.id
    stats = get_user_stats(user_id)
    
    accuracy = 0
    if stats['total_questions'] > 0:
        accuracy = (stats['correct_answers'] / stats['total_questions']) * 100
    
    stats_text = f"""
📊 <b>Подробная статистика</b>

👤 <b>Пользователь:</b> {query.from_user.first_name}

🔥 <b>Стрики:</b>
   • Текущий: <b>{stats['current_streak']}</b>
   • Рекорд: <b>{stats['best_streak']}</b>

📈 <b>Общие результаты:</b>
   • Всего вопросов: <b>{stats['total_questions']}</b>
   • Правильных ответов: <b>{stats['correct_answers']}</b>
   • Точность: <b>{accuracy:.1f}%</b>

{"🏆 <b>Отличная работа!</b>" if stats['best_streak'] >= 10 else "💪 <b>Продолжай тренироваться!</b>"}
"""
    
    await query.edit_message_text(
        stats_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_to_main_keyboard()
    )

async def start_quiz_mode(query, mode):
    """Start a quiz in the specified mode."""
    user_id = query.from_user.id
    
    try:
        # Reset lives to 3 when starting a new game
        reset_lives(user_id)
        
        question_number, question_text, source = get_random_question(mode)
        update_user_quiz_mode(user_id, mode, question_number, source)
        
        mode_names = {
            'specialty': '🎓 Специальность (15)',
            'direction': '📚 Направление (30)',
            'mixed': '🔀 Микс режим'
        }
        
        quiz_text = f"""
🎯 <b>Режим:</b> {mode_names[mode]}
"""
        
        if mode == 'mixed':
            quiz_text += f"📋 <b>Источник:</b> {get_source_display_name(source)}\n"
        
        quiz_text += f"""
❓ <b>{question_text}</b>

Введи номер этого вопроса:
"""
        
        await query.edit_message_text(
            quiz_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_quiz_control_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error starting quiz: {e}")
        await query.edit_message_text(
            "❌ Ошибка при запуске теста. Попробуй позже.",
            reply_markup=get_back_to_main_keyboard()
        )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user's answer to a quiz question."""
    user_id = update.effective_user.id
    user_answer = update.message.text.strip()
    
    stats = get_user_stats(user_id)
    
    # Check if user is in quiz mode
    if stats['quiz_mode'] == 'none':
        return
    
    # Validate answer format
    try:
        answer_num = int(user_answer)
        max_num = get_max_question_number(stats['last_question_source'])
        if answer_num < 1 or answer_num > max_num:
            await update.message.reply_text(
                f"❌ Номер вопроса должен быть от 1 до {max_num}",
                reply_markup=get_quiz_control_keyboard()
            )
            return
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введи номер вопроса (число)",
            reply_markup=get_quiz_control_keyboard()
        )
        return
    
    # Check if answer is correct
    if validate_answer(user_answer, stats['last_question_number'], stats['last_question_source']):
        # Correct answer
        result = record_correct_answer(user_id)
        
        response_text = f"✅ <b>Правильно!</b>\n\n"
        response_text += f"🔥 Стрик: <b>{result['current_streak']}</b>\n"
        response_text += f"🏆 Рекорд: <b>{result['best_streak']}</b>"
        
        if result['new_record']:
            response_text += f"\n\n🎉 <b>НОВЫЙ РЕКОРД!</b> 🎉"
        
        await update.message.reply_text(
            response_text,
            parse_mode=ParseMode.HTML
        )
        
        # Automatically continue with next question after 1 second
        import asyncio
        await asyncio.sleep(1)
        
        # Get next question
        user_id = update.effective_user.id
        stats = get_user_stats(user_id)
        
        try:
            question_number, question_text, source = get_random_question(stats['quiz_mode'])
            update_user_quiz_mode(user_id, stats['quiz_mode'], question_number, source)
            
            mode_names = {
                'specialty': '🎓 Специальность (15)',
                'direction': '📚 Направление (30)',
                'mixed': '🔀 Микс режим'
            }
            
            next_quiz_text = f"""
🎯 <b>Режим:</b> {mode_names[stats['quiz_mode']]}
"""
            
            if stats['quiz_mode'] == 'mixed':
                next_quiz_text += f"📋 <b>Источник:</b> {get_source_display_name(source)}\n"
            
            next_quiz_text += f"""
❓ <b>{question_text}</b>

Введи номер этого вопроса:
"""
            
            await update.message.reply_text(
                next_quiz_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_quiz_control_keyboard()
            )
            
        except Exception as e:
            logger.error(f"Error continuing quiz automatically: {e}")
            await update.message.reply_text(
                "❌ Ошибка при загрузке следующего вопроса",
                reply_markup=get_quiz_control_keyboard()
            )
        
    else:
        # Incorrect answer
        result = record_incorrect_answer(user_id)
        
        response_text = f"""
❌ <b>Неправильно!</b>

Правильный ответ: <b>{stats['last_question_number']}</b>

🔥 <b>Жизни:</b> {get_lives_display(result['lives_left'])}
💔 Стрик сброшен.
"""
        
        if result['game_over']:
            # Game Over - show final statistics
            final_stats = get_user_stats(user_id)
            accuracy = 0
            if final_stats['total_questions'] > 0:
                accuracy = (final_stats['correct_answers'] / final_stats['total_questions']) * 100
            
            response_text += f"""

🎮 <b>ИГРА ОКОНЧЕНА!</b>

📊 <b>Итоговая статистика:</b>
🔥 Финальный стрик: <b>{final_stats['current_streak']}</b>
🏆 Лучший результат: <b>{final_stats['best_streak']}</b>
📈 Точность: <b>{accuracy:.1f}%</b>

Попробуй ещё раз! 💪
"""
            
            await update.message.reply_text(
                response_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_game_over_keyboard()
            )
            
            # Clear quiz mode
            clear_quiz_mode(user_id)
        else:
            await update.message.reply_text(
                response_text,
                parse_mode=ParseMode.HTML
            )
            
            # Automatically continue with next question after 1 second
            import asyncio
            await asyncio.sleep(1)
            
            # Get next question
            stats = get_user_stats(user_id)
            
            try:
                question_number, question_text, source = get_random_question(stats['quiz_mode'])
                update_user_quiz_mode(user_id, stats['quiz_mode'], question_number, source)
                
                mode_names = {
                    'specialty': '🎓 Специальность (15)',
                    'direction': '📚 Направление (30)',
                    'mixed': '🔀 Микс режим'
                }
                
                next_quiz_text = f"""
🎯 <b>Режим:</b> {mode_names[stats['quiz_mode']]}
"""
                
                if stats['quiz_mode'] == 'mixed':
                    next_quiz_text += f"📋 <b>Источник:</b> {get_source_display_name(source)}\n"
                
                next_quiz_text += f"""
❓ <b>{question_text}</b>

Введи номер этого вопроса:
"""
                
                await update.message.reply_text(
                    next_quiz_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_quiz_control_keyboard()
                )
                
            except Exception as e:
                logger.error(f"Error continuing quiz automatically: {e}")
                await update.message.reply_text(
                    "❌ Ошибка при загрузке следующего вопроса",
                    reply_markup=get_quiz_control_keyboard()
                )



async def stop_quiz(query):
    """Stop the current quiz."""
    user_id = query.from_user.id
    clear_quiz_mode(user_id)
    
    stats = get_user_stats(user_id)
    
    stop_text = f"""
⏹️ <b>Тест остановлен</b>

📊 <b>Твои результаты:</b>
🔥 Текущий стрик: <b>{stats['current_streak']}</b>
🏆 Лучший результат: <b>{stats['best_streak']}</b>

Спасибо за тренировку! 💪
"""
    
    await query.edit_message_text(
        stop_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard()
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update.effective_message:
        await update.effective_message.reply_text(
            "❌ Произошла ошибка. Попробуй позже.",
            reply_markup=get_main_menu_keyboard()
        )
