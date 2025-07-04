import sqlite3
import datetime
from global_data import TABLES
from utils.time_check import is_within_working_hours
from typing import List, Tuple, Optional
from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_date_book_keyboard, get_tables_keyboard, get_time_keyboard, get_book_confirm_keyboard
from global_data import MAIN_STATE, GLOBAL_USER_DATE

# Константы
DATABASE_NAME = 'data/restaurant.db'

class DatabaseManager:
    def __init__(self, db_name: str = DATABASE_NAME):
        self.db_name = db_name

    def _get_connection(self):
        """Создаёт и возвращает соединение с базой данных"""
        return sqlite3.connect(self.db_name)

    def add_booking(
        self,
        user_id: int,
        username: str,
        table_number: int,
        booking_time: str,
        booking_hours: int = 2
    ) -> bool:
        """
        Добавляет бронирование в БД с проверкой доступности столика
        Возвращает True при успешном бронировании, False при ошибке
        """
        try:
            booking_start = datetime.datetime.strptime(booking_time, "%Y-%m-%d %H:%M")
            booking_end = booking_start + datetime.timedelta(hours=booking_hours)
            booking_end_str = booking_end.strftime("%Y-%m-%d %H:%M")

            if not self.is_table_available(table_number, booking_start, booking_end):
                return False

            with self._get_connection() as conn:
                conn.execute('''
                    INSERT INTO bookings 
                    (user_id, username, table_number, booking_time, booking_end_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, username, table_number, booking_time, booking_end_str))
            return True
        except Exception as e:
            print(f"Error adding booking: {e}")
            return False

    def is_table_available(
        self,
        table_number: int,
        start_time: datetime.datetime,
        end_time: datetime.datetime
    ) -> bool:
        """
        Проверяет, свободен ли столик в указанный промежуток времени
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 1 FROM bookings 
                    WHERE table_number = ? 
                    AND (
                        (booking_time < ? AND booking_end_time > ?) OR
                        (booking_time < ? AND booking_end_time > ?) OR
                        (booking_time >= ? AND booking_end_time <= ?)
                    )
                    LIMIT 1
                ''', (
                    table_number,
                    end_time.strftime("%Y-%m-%d %H:%M"), start_time.strftime("%Y-%m-%d %H:%M"),
                    start_time.strftime("%Y-%m-%d %H:%M"), end_time.strftime("%Y-%m-%d %H:%M"),
                    start_time.strftime("%Y-%m-%d %H:%M"), end_time.strftime("%Y-%m-%d %H:%M")
                ))
                return not cursor.fetchone()
        except Exception as e:
            print(f"Error checking table availability: {e}")
            return False

    def get_booked_tables_for_day(self, date: datetime.date) -> List[Tuple[int, str, str]]:
        """
        Возвращает список занятых столиков на указанную дату
        Формат: [(table_number, start_time, end_time), ...]
        """
        try:
            date_str = date.strftime("%Y-%m-%d")
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT table_number, booking_time, booking_end_time 
                    FROM bookings 
                    WHERE DATE(booking_time) = ?
                    ORDER BY booking_time
                ''', (date_str,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting booked tables: {e}")
            return []

    def delete_booking(self, booking_id: int) -> bool:
        """
        Удаляет бронирование по ID
        Возвращает True при успешном удалении, False при ошибке
        """
        try:
            with self._get_connection() as conn:
                conn.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
            return True
        except Exception as e:
            print(f"Error deleting booking: {e}")
            return False

    def get_user_bookings(self, user_id: int) -> List[Tuple[int, int, str, str]]:
        """
        Возвращает список бронирований пользователя
        Формат: [(booking_id, table_number, start_time, end_time), ...]
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, table_number, booking_time, booking_end_time
                    FROM bookings
                    WHERE user_id = ?
                    ORDER BY booking_time
                ''', (user_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting user bookings: {e}")
            return []


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /book"""
    try:
        db = DatabaseManager()
        user_id = update.message.from_user.id
        username = update.message.from_user.username or "Без имени"

        # Проверка количества аргументов
        if len(context.args) < 3:
            await update.message.reply_text(
                '⚠️ Используйте: /book <столик> <дата YYYY-MM-DD> <время HH:MM> [часы]\n'
            )
            return

        # Парсинг аргументов
        table_number = int(context.args[0])
        booking_date = context.args[1]
        booking_time = context.args[2]
        hours = int(context.args[3]) if len(context.args) > 3 else 2

        # Проверка столика
        if table_number not in TABLES:
            await update.message.reply_text(f'❌ Столик {table_number} не существует. Доступные: {TABLES}')
            return

        # Формирование времени бронирования
        booking_start_str = f"{booking_date} {booking_time}"
        booking_start = datetime.datetime.strptime(booking_start_str, "%Y-%m-%d %H:%M")

        # Проверка времени
        if hours < 1:
            await update.message.reply_text('⚠️ Минимальное время бронирования — 1 час.')
            return

        booking_end = booking_start + datetime.timedelta(hours=hours)
        if booking_start.date() != booking_end.date():
            await update.message.reply_text('⚠️ Бронирование не может переходить на следующий день.')
            return

        if not is_within_working_hours(booking_start, booking_end):
            await update.message.reply_text('⚠️ Бронирование вне рабочего времени.')
            return

        # Проверка и добавление бронирования
        if db.add_booking(user_id, username, table_number, booking_start_str, hours):
            await update.message.reply_text(
                f'✅ Столик {table_number} забронирован!\n'
                f'🕒 {booking_start_str} – {booking_end.strftime("%Y-%m-%d %H:%M")}'
            )
        else:
            await update.message.reply_text('❌ Этот столик уже занят на выбранное время.')

    except ValueError:
        await update.message.reply_text(
            '⚠️ Неверный формат данных. Используйте: /book <столик> <дата YYYY-MM-DD> <время HH:MM> [часы]'
        )
    except Exception as e:
        await update.message.reply_text('⚠️ Произошла ошибка при бронировании.')
        print(f"Booking error: {e}")

async def start(update, context):
    await update.message.reply_text("✏️ Выберите дату для бронирования:",
        reply_markup=get_date_book_keyboard()
    )


async def handle_book_date(update: Update, context: ContextTypes.DEFAULT_TYPE, func_name):
    global GLOBAL_USER_DATE, GLOBAL_TABLE_NUMBER, GLOBAL_USER_TIME
    query = update.callback_query if update.callback_query else None
    message = query.message if query else update.message
    user_id = update.effective_user.id
    username = update.effective_user.username or "Без имени"

    try:
        if func_name == "book_today":
            GLOBAL_USER_DATE = datetime.date.today()
        elif func_name == "book_tomorrow":
            GLOBAL_USER_DATE = datetime.date.today() + datetime.timedelta(days=1)
        elif func_name == "book_day_after":
            GLOBAL_USER_DATE = datetime.date.today() + datetime.timedelta(days=2)
        elif func_name.startswith("book_time_"):
            time_str = query.data.replace("book_time_", "")
            GLOBAL_USER_TIME = time_str
            await query.edit_message_text(
                f"🔄 Бронируем стол {GLOBAL_TABLE_NUMBER}\n"
                f"📅 На {GLOBAL_USER_DATE.strftime('%d.%m.%Y')}\n"
                f"⏰ В {time_str}\n\n"
                "Подтвердите бронирование:",
                reply_markup=get_book_confirm_keyboard()
            )

            return MAIN_STATE
        elif func_name == "book_confirm":
            table_number = GLOBAL_TABLE_NUMBER
            
            # Извлекаем время из предыдущего сообщения
            time_str = GLOBAL_USER_TIME
            booking_start_str = f"{GLOBAL_USER_DATE.strftime('%Y-%m-%d')} {time_str}"
            
            # Стандартная продолжительность брони (2 часа)
            hours = 2
            
            # Проверяем и добавляем бронирование
            db = DatabaseManager()
            if db.add_booking(user_id, username, table_number, booking_start_str, hours):
                booking_end = datetime.datetime.strptime(booking_start_str, "%Y-%m-%d %H:%M") + datetime.timedelta(hours=hours)
                
                # Удаляем предыдущее сообщение с кнопками
                await query.delete_message()
                
                # Отправляем подтверждение
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'✅ Столик {table_number} забронирован!\n'
                         f'📅 Дата: {GLOBAL_USER_DATE.strftime("%d.%m.%Y")}\n'
                         f'🕒 Время: {time_str} – {booking_end.strftime("%H:%M")}\n'
                         f'👤 Для: @{username}'
                )
            else:
                await query.edit_message_text(
                    '❌ Этот столик уже занят на выбранное время.\n'
                    'Попробуйте выбрать другое время или столик.'
                )
            return MAIN_STATE

        elif func_name == "book_cancel":
                        # Удаляем предыдущее сообщение с кнопками
            await query.delete_message()
            
            # Отправляем сообщение об отмене
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Бронирование отменено"
            )
            
            # Сбрасываем глобальные переменные
            GLOBAL_USER_DATE = None
            GLOBAL_TABLE_NUMBER = None
            GLOBAL_USER_TIME = None

            return MAIN_STATE
        else:
            val = query.data.split('_')[1]

            if val.isdigit():
                GLOBAL_TABLE_NUMBER = int(val)
                await query.edit_message_text(
                    f"✅ Стол {GLOBAL_TABLE_NUMBER}\n"
                    f"📅 {GLOBAL_USER_DATE.strftime('%d.%m.%Y')}\n"
                    "⏰ Выберите время:",
                    reply_markup=get_time_keyboard()
                )
            else:
                await message.reply_text(
                    "🪑Выберите номер столика",
                    reply_markup=get_tables_keyboard()
                )   
            return MAIN_STATE

        await message.reply_text(
                "🪑Выберите номер столика",
                reply_markup=get_tables_keyboard()
            )
        return MAIN_STATE
    except Exception as e:
        print(f"Ошибка в handle_date_choice: {e}")
        await message.reply_text("⚠️ Произошла ошибка при обработке запроса")
        return MAIN_STATE