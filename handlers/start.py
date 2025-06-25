from utils.keyboards import get_main_keyboard

async def handler(update, context):
    await update.message.reply_text(
        '👋 Привет! Я бот для бронирования столиков',
        reply_markup=get_main_keyboard()
    )