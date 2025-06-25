from config import RESTAURANT_OPEN_TIME, RESTAURANT_CLOSE_TIME

def is_within_working_hours(start_time, end_time):
    return (
        start_time.date() == end_time.date() and
        RESTAURANT_OPEN_TIME <= start_time.hour < RESTAURANT_CLOSE_TIME and
        RESTAURANT_OPEN_TIME < end_time.hour <= RESTAURANT_CLOSE_TIME
    )
