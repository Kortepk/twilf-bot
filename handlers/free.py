import sqlite3
import datetime
from config import TABLES, RESTAURANT_OPEN_TIME, RESTAURANT_CLOSE_TIME

async def handler(update, context):
    try:
        date_str = context.args[0]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT table_number, booking_time, booking_end_time FROM bookings WHERE DATE(booking_time) = ?', (date,))
        bookings = cursor.fetchall()
        conn.close()

        slots = [
            datetime.datetime.combine(date, datetime.time(h, m))
            for h in range(RESTAURANT_OPEN_TIME, RESTAURANT_CLOSE_TIME)
            for m in range(0, 60, 10)
        ]

        availability = {}
        for slot in slots:
            free = []
            for table in TABLES:
                busy = any(
                    int(b[0]) == table and
                    datetime.datetime.strptime(b[1], "%Y-%m-%d %H:%M") <= slot <
                    datetime.datetime.strptime(b[2], "%Y-%m-%d %H:%M")
                    for b in bookings
                )
                if not busy:
                    free.append(table)
            if free:
                availability[slot.strftime("%H:%M")] = free

        if availability:
            msg = f'📅 *Свободные столики на {date_str}:*\n\n'
            for time, tables in availability.items():
                msg += f'🕒 {time}: {tables}\n'
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text("😔 Нет свободных столиков на этот день.")
    except Exception:
        await update.message.reply_text('⚠️ Используйте: /free <дата YYYY-MM-DD>')
