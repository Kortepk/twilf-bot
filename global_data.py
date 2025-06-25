import datetime
RESTAURANT_OPEN_TIME = 10
RESTAURANT_CLOSE_TIME = 22
TABLES = list(range(1, 13))

# Состояния бота
MAIN_STATE = 1  # Основное состояние (можно использовать любые команды)
DATE_INPUT_STATE = 2  # Состояние ввода даты (только дата или отмена)

GLOBAL_USER_DATE = datetime.date.today()