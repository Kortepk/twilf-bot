import sqlite3
from config import ADMIN_USER_ID

async def start(update, context):
    await update.message.reply_text("🆔 Введите команду: /cancel <ID>")

async def handler(update, context):
    try:
        booking_id = int(context.args[0])
        user_id = update.message.from_user.id

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM bookings WHERE id = ?', (booking_id,))
        booking = cursor.fetchone()

        if booking:
            if user_id == booking[0] or user_id == ADMIN_USER_ID:
                cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
                conn.commit()
                await update.message.reply_text(f'🗑️ Бронирование {booking_id} отменено.')
            else:
                await update.message.reply_text('🚫 У вас нет прав отменить это бронирование.')
        else:
            await update.message.reply_text('❌ Бронирование не найдено.')

        conn.close()
    except (IndexError, ValueError):
        await update.message.reply_text('⚠️ Используйте: /cancel <ID>')