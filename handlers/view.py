import sqlite3
from config import ADMIN_USER_ID

async def handler(update, context):
    user_id = update.message.from_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text('🚫 Нет доступа.')
        return

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()

    if bookings:
        response = "📋 *Все бронирования:*\n"
        for b in bookings:
            response += f"🆔 {b[0]} | 👤 @{b[2]} | 🍽️ Столик {b[3]}\n🕒 {b[4]} – {b[5]}\n\n"
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        await update.message.reply_text('📭 Бронирований нет.')