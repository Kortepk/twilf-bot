from telegram.ext import Application
from config import BOT_TOKEN
from db import init_db
from handlers.init import register_handlers

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    register_handlers(app)
    app.run_polling()

if __name__ == '__main__':
    main()