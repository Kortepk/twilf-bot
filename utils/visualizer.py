from PIL import Image, ImageDraw, ImageFont
import datetime
from global_data import TABLES, RESTAURANT_OPEN_TIME, RESTAURANT_CLOSE_TIME
from typing import List, Tuple

class BookingVisualizer:
    def __init__(self):
        self.cell_width = 100
        self.cell_height = 30
        self.header_height = 50
        self.time_column_width = 80
        self.font_path = "arial.ttf"
        self.border_color = (100, 100, 100)

        # Цветовая схема (пастельные красные тона)
        self.background_color = (255, 240, 240)  # Фон
        self.header_color = (255, 200, 200)      # Заголовок 
        self.grid_color = (255, 160, 160)        # Линии сетки
        self.booked_color = (255, 120, 120)     # Занятые ячейки
        self.text_color = (100, 0, 0)            # Текст
        self.table_bg_color = (255, 255, 255)    # Фон таблицы

        self.general_header_font_size = 30
        self.header_font_size = 16
        self.column_font_size = 16
        
    def _get_font(self, size):
        try:
            return ImageFont.truetype(self.font_path, size)
        except:
            return ImageFont.load_default(size=size)

    def _get_text_size(self, draw, text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def _get_time_slots(self):
        slots = []
        for hour in range(RESTAURANT_OPEN_TIME, RESTAURANT_CLOSE_TIME):
            for minute in range(0, 60, 30):
                time = datetime.time(hour, minute)
                slots.append(time.strftime("%H:%M")
                             )
        time = datetime.time(RESTAURANT_CLOSE_TIME, 0)
        slots.append(time.strftime("%H:%M"))

        return slots

    def _draw_header(self, draw, image_width, title):
        font = self._get_font(self.general_header_font_size)
        text_width, text_height = self._get_text_size(draw, title, font)
        
        # Фон заголовка (пастельный розовый)
        draw.rectangle(
            [(0, 0), (image_width, self.header_height)],
            fill=self.header_color
        )
        
        draw.text(
            ((image_width - text_width) // 2, (self.header_height - text_height) // 2),
            title,
            font=font,
            fill=self.text_color  # Темно-красный текст
        )

    def _draw_table_grid(self, draw, image_width, image_height, time_slots):
        # Вертикальные линии
        for i, table in enumerate(TABLES):
            x = self.time_column_width + i * self.cell_width
            draw.line([(x, self.header_height), (x, image_height)], fill=self.border_color)

        # Горизонтальные линии
        for i in range(len(time_slots) + 1):
            y = self.header_height + i * self.cell_height
            draw.line([(0, y), (image_width, y)], fill=self.border_color)

    def _draw_time_column(self, draw, time_slots):
        font = self._get_font(self.column_font_size)
        for i, time in enumerate(time_slots):
            y = self.header_height + (i+1) * self.cell_height + (self.cell_height - 10) // 2
            draw.text((10, y), time, font=font, fill=self.text_color)

    def _draw_table_headers(self, draw):
        font = self._get_font(self.header_font_size )
        for i, table in enumerate(TABLES):
            x = self.time_column_width + i * self.cell_width + 10
            y = self.header_height + 5
            draw.text((x, y), f"Стол {table}", font=font, fill=self.text_color)

    def _highlight_booked_slots(self, draw, bookings):
        time_slots = self._get_time_slots()
        for table, start_str, end_str in bookings:
            if table not in TABLES:
                continue
                
            start_time = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M").time()
            end_time = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M").time()
            
            table_index = TABLES.index(table)
            x1 = self.time_column_width + table_index * self.cell_width
            x2 = x1 + self.cell_width
            
            for i, slot_time in enumerate(time_slots):
                slot_time_obj = datetime.datetime.strptime(slot_time, "%H:%M").time()
                y1 = self.header_height + (i+1) * self.cell_height
                y2 = y1 + self.cell_height
                
                if start_time <= slot_time_obj < end_time:
                        draw.rectangle([x1, y1, x2, y2], fill=self.booked_color)  # Пастельный красный
                        
    def generate_booking_image(self, title: str, bookings: List[Tuple[int, str, str]]) -> Image.Image:
        time_slots = self._get_time_slots()
        image_width = self.time_column_width + len(TABLES) * self.cell_width
        image_height = self.header_height + (len(time_slots) + 1) * self.cell_height
        
        # Создаем изображение с зеленым фоном
        image = Image.new("RGB", (image_width, image_height), self.background_color)
        draw = ImageDraw.Draw(image)
        
        # Рисуем белую область для таблицы
        draw.rectangle(
            [
                (self.time_column_width, self.header_height),
                (image_width, image_height)
            ],
            fill="white"
        )
        
        # Отрисовываем элементы таблицы
        self._draw_header(draw, image_width, title)
        self._draw_table_grid(draw, image_width, image_height, time_slots)
        self._draw_time_column(draw, time_slots)
        self._draw_table_headers(draw)
        self._highlight_booked_slots(draw, bookings)
        
        return image