from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import datetime
from global_data import TABLES, RESTAURANT_OPEN_TIME, RESTAURANT_CLOSE_TIME

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

def get_time_keyboard():
    """Генерирует клавиатуру с временными слотами 10:00-22:00 с шагом 30 минут"""
    time_slots = []
    current_time = datetime.time(RESTAURANT_OPEN_TIME, 0)  # Начинаем с 10:00
    
    while current_time.hour < RESTAURANT_CLOSE_TIME:
        time_str = current_time.strftime("%H:%M")
        time_slots.append(
            InlineKeyboardButton(time_str, callback_data=f"book_time_{time_str}")
        )
        
        # Увеличиваем время на 30 минут
        new_minute = current_time.minute + 30
        new_hour = current_time.hour + (new_minute // 60)
        new_minute = new_minute % 60
        current_time = datetime.time(new_hour, new_minute)
    
    # Разбиваем кнопки на ряды по 4
    keyboard = [time_slots[i:i+4] for i in range(0, len(time_slots), 4)]
    
    return InlineKeyboardMarkup(keyboard)

def get_book_confirm_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Подтвердить", callback_data="book_confirm")],
        [InlineKeyboardButton("❌ Отменить", callback_data="book_acncel")]
    ])
