"""
Quiz data management module
Contains exam questions and handles question selection logic
"""

import random
from typing import Tuple, List

# Questions from the first file (Specialty - 15 questions)
SPECIALTY_QUESTIONS = [
    "Business Model Canvas – Definition",
    "What is the concept of breakthrough innovation and disruptive innovation?",
    "Present the concept of value innovation and a four-action strategy for building a new market space",
    "Present the concept of the knowledge illusion or the leader's dilemma in forecasting. concepts.",
    "Networks in strategic management. Explain the notion and types of inter- organizational networks.",
    "The Black swan theory and its characteristics. Give examples of phenomena that can be classified as Black swans.",
    "The Lean Startup method. What innovative tools for creating new businesses do you know?",
    "What is a competitive advantage? When it makes sense to focus the company's activity in a selected segment?",
    "Explain the long tail strategy and give examples of companies that use the long tail in their strategic activities.",
    "What is the sharing economy? How does it relate to the decline of capitalism?",
    "Explain the notion of the \"problem of the second half of the chessboard\" and how it is related to the organization's business strategy.",
    "What is the structure of inequality and global wealth inequality in the 21st century?",
    "What is the iterative process of creating a business concept?",
    "Characterize and explain the principles of Agile operations as a method of managing an organization.",
    "What is the Continuous Improvement process and Lean Process Development?"
]

# Questions from the second file (Direction - 30 questions)
DIRECTION_QUESTIONS = [
    "Basic Functions of Management:",
    "Globalization in World Markets:",
    "Structure and characteristics of managerial competencies. Give characteristics of 3 structures of your choice.",
    "Entrepreneurship – the notion, its characteristics and conditions for its development in modern economies.",
    "Competitiveness, competitive potential and competitive advantage – notions and determinants.",
    "Business ethics – manifestation of unethical practices and preventing measures.",
    "IT systems and their use in organizational management.",
    "Market environment and its role for an organization.",
    "Factors influencing consumer's behavior in the market. Discuss one of them.",
    "Notions, components and use of the SWOT and the TOWS analysis.",
    "Give one traditional and one contemporary definition of marketing. Give examples.",
    "List organizational methods and techniques. Describe a selected method and technique.",
    "What are the components of a marketing plan? Discuss shortly the components and their purpose.",
    "Pricing strategies and their determining factors.",
    "Product and its life cycle in the market – description of its stages and its implications for acompany.",
    "List the tools of integrated marketing communication.",
    "Classification of costs in accounting.",
    "Functions and structure of a business plan.",
    "The difference between vision, mission and strategy of an organization. Give examples of vision and mission.",
    "The essence of enterprise strategy and types of strategies.",
    "The meaning and essence of project management in contemporary organizations.",
    "Functions and tools of human resource management (HRM).",
    "Basic motivation theories and instruments.",
    "Classical and contemporary models of organizational structures. Give examples.",
    "The basic management styles used by managers.",
    "Please discuss the principles of functioning of market economy",
    "Please discuss the basic directions of the Balcerowicz Plan and its social and economic impact.",
    "The impact of taxes, government grants and loans on operating a business.",
    "The effects of introducing protective customs tariffs and minimum and maximum prices.",
    "Please indicate short- and long-term effects of inflation."
]

def get_random_question(mode: str) -> Tuple[int, str, str]:
    """
    Get a random question based on the selected mode.
    
    Args:
        mode: 'specialty', 'direction', or 'mixed'
    
    Returns:
        Tuple of (question_number, question_text, source)
    """
    if mode == 'specialty':
        question_number = random.randint(1, len(SPECIALTY_QUESTIONS))
        question_text = SPECIALTY_QUESTIONS[question_number - 1]
        source = 'specialty'
    elif mode == 'direction':
        question_number = random.randint(1, len(DIRECTION_QUESTIONS))
        question_text = DIRECTION_QUESTIONS[question_number - 1]
        source = 'direction'
    elif mode == 'mixed':
        # Randomly choose between specialty and direction
        if random.choice([True, False]):
            question_number = random.randint(1, len(SPECIALTY_QUESTIONS))
            question_text = SPECIALTY_QUESTIONS[question_number - 1]
            source = 'specialty'
        else:
            question_number = random.randint(1, len(DIRECTION_QUESTIONS))
            question_text = DIRECTION_QUESTIONS[question_number - 1]
            source = 'direction'
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    return question_number, question_text, source

def validate_answer(answer: str, expected_number: int, source: str) -> bool:
    """
    Validate if the user's answer matches the expected question number.
    
    Args:
        answer: User's answer as string
        expected_number: Expected question number
        source: Source of the question ('specialty' or 'direction')
    
    Returns:
        True if answer is correct, False otherwise
    """
    try:
        user_answer = int(answer.strip())
        return user_answer == expected_number
    except ValueError:
        return False

def get_source_display_name(source: str) -> str:
    """Get display name for question source."""
    if source == 'specialty':
        return "Специальность (15 вопросов)"
    elif source == 'direction':
        return "Направление (30 вопросов)"
    else:
        return "Неизвестный источник"

def get_max_question_number(source: str) -> int:
    """Get maximum question number for the given source."""
    if source == 'specialty':
        return len(SPECIALTY_QUESTIONS)
    elif source == 'direction':
        return len(DIRECTION_QUESTIONS)
    else:
        return 0
