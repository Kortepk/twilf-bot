from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from handlers import start, book, cancel, view, mybookings, free, text_routes

from handlers.free import *

def register_handlers(app):


    #app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_routes.fallback))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start.handler)],  # Команда запуска
        states={
            MAIN_STATE: [
                # Разрешаем все команды в основном состоянии
                CommandHandler("start", start.handler),
                CommandHandler("book", book.handler),
                CommandHandler("cancel", cancel.handler),
                CommandHandler("view", view.handler),
                CommandHandler("mybookings", mybookings.handler),
                CommandHandler("free", free.handler),
                CallbackQueryHandler(handle_date_choice),
                MessageHandler(filters.TEXT & ~filters.COMMAND, text_routes.fallback)
            ],
            DATE_INPUT_STATE: [
                # Разрешаем только ввод даты или отмену
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_manual_date),
                CallbackQueryHandler(free.cancel_handler)
            ]
        },
        fallbacks=[CommandHandler('cancel', free.cancel_handler)],
        per_chat=True,
        per_user=True
    )
    
    app.add_handler(conv_handler)