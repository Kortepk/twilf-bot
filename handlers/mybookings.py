import sqlite3

async def handler(update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, table_number, booking_time, booking_end_time FROM bookings WHERE user_id = ?', (user_id,))
    bookings = cursor.fetchall()
    conn.close()

    if bookings:
        response = "📋 *Ваши бронирования:*\n"
        for b in bookings:
            response += f"🆔 {b[0]} | 🍽️ Столик {b[1]}\n🕒 {b[2]} – {b[3]}\n\n"
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        await update.message.reply_text('❌ У вас нет активных бронирований.')


