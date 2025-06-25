from handlers import mybookings, free, cancel, book

async def fallback(update, context):
    text = update.message.text.strip()

    if "Забронировать" in text:
        await book.start(update, context)

    elif "Мои бронирования" in text:
        await mybookings.handler(update, context)

    elif "Отменить" in text:
        await cancel.start(update, context)

    elif "Свободные столики" in text:
        await free.handler(update, context)

    else:
        await update.message.reply_text("❓ Неизвестная команда. Нажмите на кнопку или используйте /start")
