from telegram.ext import CommandHandler, MessageHandler, filters
from handlers import start, book, cancel, view, mybookings, free, text_routes

def register_handlers(app):
    app.add_handler(CommandHandler("start", start.handler))
    app.add_handler(CommandHandler("book", book.handler))
    app.add_handler(CommandHandler("cancel", cancel.handler))
    app.add_handler(CommandHandler("view", view.handler))
    app.add_handler(CommandHandler("mybookings", mybookings.handler))
    app.add_handler(CommandHandler("free", free.handler))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_routes.fallback))