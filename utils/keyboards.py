from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["🍽️ Забронировать", "❌ Отменить бронь"],
            ["📋 Мои бронирования", "📅 Свободные столики"]
        ],
        resize_keyboard=True
    )

def get_cancel_inline(booking_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="❌ Отменить бронь", callback_data=f"cancel:{booking_id}")]
    ])