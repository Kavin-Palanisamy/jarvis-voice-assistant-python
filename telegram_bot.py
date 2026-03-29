import os
import threading
from dotenv import load_dotenv

try:
    import telebot
except ImportError:
    telebot = None
    print("Warning: 'pyTelegramBotAPI' not installed. Telegram remote control disabled.")

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# We'll import execute_task inside the handler to avoid circular imports if any
import task_engine as te

bot = telebot.TeleBot(TELEGRAM_TOKEN) if (telebot and TELEGRAM_TOKEN) else None

if bot:
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        """Receives commands from Telegram and executes them via JARVIS task engine."""
        command = message.text
        print(f"Telegram command received: {command}")
        
        # Process the command using JARVIS's task engine
        from command_parser import split_into_tasks, clean_task
        import task_engine as te
        
        tasks = split_into_tasks(command)
        cleaned_tasks = [clean_task(t) for t in tasks]
        
        responses = []
        for task in cleaned_tasks:
            response = te.execute_task(task)
            if response:
                responses.append(response)
        
        final_response = "\n".join(responses) if responses else "Command acknowledged, Sir."
        bot.reply_to(message, final_response)
else:
    def handle_message(message):
        pass

def start_telegram_bot():
    """Runs the Telegram bot listener in a background thread."""
    if not bot:
        print("Telegram Bot disabled (missing library or TELEGRAM_BOT_TOKEN in .env).")
        return
        
    print("Telegram Bot is online. Monitoring for remote commands...")
    bot_thread = threading.Thread(target=bot.infinity_polling, daemon=True)
    bot_thread.start()

if __name__ == "__main__":
    # start_telegram_bot()
    # while True: time.sleep(1)
    pass
