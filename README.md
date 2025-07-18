# Telegram Quiz Bot

## Description
A Telegram bot for testing knowledge of exam question numbers with an intuitive button interface, life system, and statistics tracking.

## Features
- 🎯 Button-based interface (no commands needed)
- 🔥 3-lives system with visual indicators
- 📊 Statistics tracking with streaks and records
- 🎓 Three quiz modes: Specialty (15 questions), Direction (30 questions), and Mixed mode
- 🌍 Russian language interface
- 🔄 Automatic question progression
- 📈 Personal performance tracking

## Local Development

### Prerequisites
- Python 3.11+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r railway_requirements.txt
   ```

3. Set environment variable:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## Railway Deployment

### Step 1: Prepare Your Repository
1. Upload all files to your GitHub repository
2. Make sure you have these files:
   - `main.py` - Main bot application
   - `database.py` - Database management
   - `handlers.py` - Bot message handlers
   - `keyboards.py` - Inline keyboards
   - `quiz_data.py` - Quiz questions and logic
   - `railway_requirements.txt` - Python dependencies
   - `Procfile` - Railway process file
   - `runtime.txt` - Python version specification
   - `railway.json` - Railway configuration

### Step 2: Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will automatically detect it's a Python project

### Step 3: Set Environment Variables
1. In Railway dashboard, go to your project
2. Click on "Variables" tab
3. Add environment variable:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Your bot token from BotFather

### Step 4: Deploy
1. Railway will automatically build and deploy your bot
2. Check the logs to ensure it's running
3. Your bot should be online and ready to use!

## Project Structure
```
telegram-quiz-bot/
├── main.py                    # Bot entry point
├── database.py               # SQLite database management
├── handlers.py               # Message and callback handlers
├── keyboards.py              # Inline keyboard layouts
├── quiz_data.py              # Quiz questions and logic
├── railway_requirements.txt  # Python dependencies
├── Procfile                  # Railway process configuration
├── runtime.txt               # Python version
├── railway.json              # Railway deployment config
└── README.md                 # This file
```

## Bot Commands
- `/start` - Start the bot and see main menu
- `/help` - Show help information

## Quiz Modes
- **Specialty (15)** - Questions 1-15 about business strategy and innovation
- **Direction (30)** - Questions 1-30 about management and economics
- **Mixed Mode** - Random questions from both categories

## Game Rules
- Start with 3 lives (❤️❤️❤️)
- Correct answers continue the game and build streaks
- Wrong answers remove a life (❤️❤️🖤)
- Game ends when all lives are lost
- Statistics track performance and records

## Database
- SQLite database (`quiz_bot.db`) stores user data
- Automatic database migration for new columns
- User statistics and game state persistence

## Error Handling
- Comprehensive error logging
- Graceful degradation for database issues
- User-friendly error messages in Russian

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
This project is for educational purposes.

## Support
For issues or questions, check the Railway logs or GitHub issues.