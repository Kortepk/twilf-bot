from global_data import MAIN_STATE, DATE_INPUT_STATE
from telegram import Update
from telegram.ext import ContextTypes
from handlers.free import handle_date_choice
from handlers.book import handle_book_date

async def handle_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  
    
    func_name = query.data
    print(f"Получен callback: {func_name}")

    try:  
        if func_name.startswith("free_"):
            # Передаем и update, и context в handle_date_choice
            return await handle_date_choice(update, func_name)
        
        elif func_name.startswith("book_"):
            return await handle_book_date(update, func_name)
            
    except Exception as e:
        error_msg = f"⚠️ Ошибка: {str(e)}"
        if update.callback_query:
            await update.callback_query.message.reply_text(error_msg)
        elif update.message:
            await update.message.reply_text(error_msg)
        return MAIN_STATE

    return MAIN_STATE
