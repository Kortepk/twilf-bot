import sqlite3
import datetime
from config import TABLES
from utils.time_check import is_within_working_hours


async def start(update, context):
    await update.message.reply_text("✏️ Введите команду: /book <столик> <дата> <время> <часы>")


async def handler(update, context):
    try:
        table_number = int(context.args[0])
        booking_start_str = context.args[1] + ' ' + context.args[2]
        hours = int(context.args[3])
        user_id = update.message.from_user.id
        username = update.message.from_user.username

        if table_number not in TABLES:
            await update.message.reply_text(f'❌ Столик {table_number} не существует. Доступные: {TABLES}')
            return

        booking_start = datetime.datetime.strptime(booking_start_str, "%Y-%m-%d %H:%M")
        booking_end = booking_start + datetime.timedelta(hours=hours)

        if hours < 1:
            await update.message.reply_text('⚠️ Минимальное время бронирования — 1 час.')
            return

        if booking_start.date() != booking_end.date():
            await update.message.reply_text('⚠️ Бронирование не может переходить на следующий день.')
            return

        if not is_within_working_hours(booking_start, booking_end):
            await update.message.reply_text('⚠️ Бронирование вне рабочего времени.')
            return

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM bookings 
            WHERE table_number = ? 
            AND ((booking_time <= ? AND booking_end_time > ?) 
            OR (booking_time < ? AND booking_end_time >= ?))
        ''', (
            table_number,
            booking_start_str, booking_start_str,
            booking_end.strftime("%Y-%m-%d %H:%M"), booking_end.strftime("%Y-%m-%d %H:%M")
        ))
        if cursor.fetchall():
            await update.message.reply_text('❌ Этот столик уже занят на выбранное время.')
            conn.close()
            return

        cursor.execute('''
            INSERT INTO bookings (user_id, username, table_number, booking_time, booking_end_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, table_number, booking_start_str, booking_end.strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()

        await update.message.reply_text(
            f'✅ Столик {table_number} забронирован!\n🕒 {booking_start_str} – {booking_end.strftime("%Y-%m-%d %H:%M")}'
        )
    except (IndexError, ValueError):
        await update.message.reply_text('⚠️ Используйте: /book <столик> <дата YYYY-MM-DD> <время HH:MM> <часы>')