import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Verify token is set
if not BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"Hi {user.first_name}! 👋\n\n"
        f"I'm a simple echo bot. Send me any message and I'll echo it back!\n\n"
        f"Available commands:\n"
        f"/start - Start the bot\n"
        f"/help - Show this help message\n"
        f"/echo <text> - Echo your text\n"
        f"/about - About this bot"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when the command /help is issued."""
    help_text = (
        "🤖 Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/echo <text> - Echo your text back\n"
        "/about - Learn about this bot\n\n"
        "Or just send me any text and I'll echo it!"
    )
    await update.message.reply_text(help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    # Get the text after /echo command
    if context.args:
        text_to_echo = ' '.join(context.args)
        await update.message.reply_text(f"🔊 Echo: {text_to_echo}")
    else:
        await update.message.reply_text("Please provide text to echo. Example: /echo Hello World!")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send information about the bot."""
    about_text = (
        "🤖 **About This Bot**\n\n"
        "This is a simple Telegram echo bot built with python-telegram-bot.\n\n"
        "**Features:**\n"
        "• Echoes any message you send\n"
        "• Responds to commands\n"
        "• Shows user info\n\n"
        "**Technology Stack:**\n"
        "• Python 3.11+\n"
        "• python-telegram-bot v20.7\n"
        "• Deployed on Railway\n\n"
        "Made with ❤️ for Telegram"
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo any text message."""
    user_text = update.message.text
    user_name = update.effective_user.first_name
    
    response = f"📝 You said: {user_text}\n\n👤 From: {user_name}"
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("about", about))
    
    # Register message handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot (polling)
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
