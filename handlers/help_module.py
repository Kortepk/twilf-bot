from utils.keyboards import get_main_keyboard

async def handler(update, context):
    await update.message.reply_text(
        '🛎️ *Доступные команды:*\n'
        '/start — Приветствие\n'
        '/book <столик> <дата> <время> <часы> — Забронировать 🍽️\n'
        '/cancel <ID> — Отменить бронь ❌\n'
        '/mybookings — Мои бронирования 📋\n'
        '/view — Все брони (админ) 🔒\n'
        '/free <дата> — Свободные столики 📅',
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )
