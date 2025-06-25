from utils.keyboards import get_main_keyboard

from global_data import MAIN_STATE

async def handler(update, context):
    await update.message.reply_text(
        '👋 Привет! Я бот для бронирования столиков',
        reply_markup=get_main_keyboard()
    )
    return MAIN_STATE