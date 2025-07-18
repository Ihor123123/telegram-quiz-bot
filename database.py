"""
Database module for handling user statistics and quiz data
"""

import sqlite3
import logging
from contextlib import contextmanager
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

DATABASE_FILE = 'quiz_bot.db'

def init_database():
    """Initialize the SQLite database with required tables."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        
        # Create users table for statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                total_questions INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                quiz_mode TEXT DEFAULT 'none',
                last_question_number INTEGER DEFAULT 0,
                last_question_source TEXT DEFAULT '',
                lives_left INTEGER DEFAULT 3
            )
        ''')
        
        # Check if lives_left column exists and add it if it doesn't
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'lives_left' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN lives_left INTEGER DEFAULT 3')
            logger.info("Added lives_left column to existing users table")
        
        conn.commit()
        logger.info("Database initialized successfully")

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()

def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Get user statistics from database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        else:
            # Create new user record
            cursor.execute('''
                INSERT INTO users (user_id, current_streak, best_streak, total_questions, correct_answers, lives_left)
                VALUES (?, 0, 0, 0, 0, 3)
            ''', (user_id,))
            conn.commit()
            return {
                'user_id': user_id,
                'username': None,
                'first_name': None,
                'current_streak': 0,
                'best_streak': 0,
                'total_questions': 0,
                'correct_answers': 0,
                'quiz_mode': 'none',
                'last_question_number': 0,
                'last_question_source': '',
                'lives_left': 3
            }

def update_user_info(user_id: int, username: str = None, first_name: str = None):
    """Update user information."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET username = ?, first_name = ?
            WHERE user_id = ?
        ''', (username, first_name, user_id))
        conn.commit()

def update_user_quiz_mode(user_id: int, quiz_mode: str, question_number: int = 0, question_source: str = ''):
    """Update user's current quiz mode and question."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET quiz_mode = ?, last_question_number = ?, last_question_source = ?
            WHERE user_id = ?
        ''', (quiz_mode, question_number, question_source, user_id))
        conn.commit()

def record_correct_answer(user_id: int) -> Dict[str, Any]:
    """Record a correct answer and update streaks."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get current stats
        cursor.execute('SELECT current_streak, best_streak FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            current_streak = row['current_streak'] + 1
            best_streak = max(row['best_streak'], current_streak)
            new_record = current_streak > row['best_streak']
            
            # Update stats
            cursor.execute('''
                UPDATE users 
                SET current_streak = ?, best_streak = ?, total_questions = total_questions + 1, 
                    correct_answers = correct_answers + 1
                WHERE user_id = ?
            ''', (current_streak, best_streak, user_id))
            conn.commit()
            
            return {
                'current_streak': current_streak,
                'best_streak': best_streak,
                'new_record': new_record
            }
        
        return {'current_streak': 0, 'best_streak': 0, 'new_record': False}

def record_incorrect_answer(user_id: int) -> Dict[str, Any]:
    """Record an incorrect answer, reset current streak, and remove a life."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get current lives
        cursor.execute('SELECT lives_left FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            lives_left = max(0, row['lives_left'] - 1)
            game_over = lives_left == 0
            
            # Update stats
            cursor.execute('''
                UPDATE users 
                SET current_streak = 0, total_questions = total_questions + 1, lives_left = ?
                WHERE user_id = ?
            ''', (lives_left, user_id))
            conn.commit()
            
            return {
                'lives_left': lives_left,
                'game_over': game_over
            }
        
        return {'lives_left': 0, 'game_over': True}

def clear_quiz_mode(user_id: int):
    """Clear user's quiz mode when stopping the test."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET quiz_mode = 'none', last_question_number = 0, last_question_source = '', lives_left = 3
            WHERE user_id = ?
        ''', (user_id,))
        conn.commit()

def reset_lives(user_id: int):
    """Reset user's lives to 3 when starting a new game."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET lives_left = 3
            WHERE user_id = ?
        ''', (user_id,))
        conn.commit()

def get_lives_display(lives_left: int) -> str:
    """Get display string for lives left."""
    heart_full = "❤️"
    heart_empty = "🖤"
    
    display = ""
    for i in range(3):
        if i < lives_left:
            display += heart_full
        else:
            display += heart_empty
    
    return display
