from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from global_data import TABLES

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


def get_date_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Сегодня", callback_data="free_today"),
            InlineKeyboardButton("Завтра", callback_data="free_tomorrow")
        ],
        [
            InlineKeyboardButton("Послезавтра", callback_data="free_day_after"),
            InlineKeyboardButton("Другая дата", callback_data="free_custom")
        ]
    ])
    
def get_cancel_keyboard():
    return InlineKeyboardMarkup([
        [  
            InlineKeyboardButton("❌ Отмена", callback_data="cancel_input")
        ]
    ])

def get_date_book_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Сегодня", callback_data="book_today"),
            InlineKeyboardButton("Завтра", callback_data="book_tomorrow")
        ],
        [
            InlineKeyboardButton("Послезавтра", callback_data="book_day_after")
        ]
    ])

def get_tables_keyboard(prefix: str = "book_") -> InlineKeyboardMarkup:
    buttons_per_row = 4  # Количество кнопок в одном ряду
    keyboard = []
    
    # Разбиваем столики на ряды
    for i in range(0, len(TABLES), buttons_per_row):
        row = [
            InlineKeyboardButton(
                f"Стол {table}", 
                callback_data=f"{prefix}{table}"
            )
            for table in TABLES[i:i + buttons_per_row]
        ]
        keyboard.append(row)

    
    return InlineKeyboardMarkup(keyboard)