import datetime

from global_data import MAIN_STATE, DATE_INPUT_STATE

from utils.keyboards import get_date_keyboard, get_cancel_keyboard

from telegram import Update
from telegram.ext import ContextTypes

from handlers.book import DatabaseManager

async def handler(update, context):

    await update.message.reply_text(
        "📅 Выберите дату для просмотра свободных столиков:",
        reply_markup=get_date_keyboard()
    )

    return MAIN_STATE

async def handle_date_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  
    
    func_name = query.data

    print(query.data)

    try:
        if func_name == "free_today":
            date = datetime.date.today()
        elif func_name == "free_tomorrow":
            date = datetime.date.today() + datetime.timedelta(days=1)
        elif func_name == "free_day_after":
            date = datetime.date.today() + datetime.timedelta(days=2)
        elif func_name == "free_custom":
            await query.edit_message_text(
                "Введите дату в формате ДД.ММ.ГГГГ", 
                reply_markup=get_cancel_keyboard()
            ) 
            return DATE_INPUT_STATE
        
        db = DatabaseManager()
        booked_tables = db.get_booked_tables_for_day(datetime.date.today())

        await query.edit_message_text(
            f"Вы выбрали: {date.strftime('%d.%m.%Y')}\n"
            f"Занятые столики: {booked_tables}"  
        )
    except Exception as e:
        await query.edit_message_text(f"Ошибка: {str(e)}")

    return MAIN_STATE  # Возвращаем в основное состояние

async def handle_manual_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ручного ввода даты"""
    try:
        day, month, year = map(int, update.message.text.split('.'))
        date = datetime.date(year, month, day)
        
        # Проверка что дата не в прошлом
        if date < datetime.date.today():
            await update.message.reply_text("❌ Нельзя выбрать прошедшую дату. Попробуйте снова:",
                reply_markup=get_cancel_keyboard()
            )
            return DATE_INPUT_STATE
            
        await update.message.reply_text(f"Выбрана дата: {date.strftime('%d.%m.%Y')}")
        return MAIN_STATE  # Возвращаем в основное состояние
        
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Неверный формат. Введите дату как ДД.ММ.ГГГГ:",
            reply_markup=get_cancel_keyboard()
        )
        return DATE_INPUT_STATE

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:  # Если отмена через инлайн-кнопку
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("❌ Ввод даты отменён")
    elif update.message:  # Если отмена через команду /cancel
        await update.message.reply_text("❌ Ввод даты отменён")
    
    return MAIN_STATE