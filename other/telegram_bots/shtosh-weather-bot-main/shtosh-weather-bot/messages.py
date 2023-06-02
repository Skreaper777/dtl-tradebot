from api_service import get_weather
from coordinates import get_coordinates


def weather() -> str:
    """Returns a message about the temperature and weather description"""
    wthr = get_weather(get_coordinates())
    return f'{wthr.location}, {wthr.description}\n' \
           f'Temperature is {wthr.temperature}°C, feels like {wthr.temperature_feeling}°C'


def wind() -> str:
    """Returns a message about wind direction and speed"""
    wthr = get_weather(get_coordinates())
    return f'{wthr.wind_direction} ветер {wthr.wind_speed} м/с'


def sun_time() -> str:
    """Returns a message about the time of sunrise and sunset"""
    wthr = get_weather(get_coordinates())
    return f'Восход: {wthr.sunrise.strftime("%H:%M")}\n' \
           f'Закат: {wthr.sunset.strftime("%H:%M")}\n'

def my_msg() -> str:
    """Returns a message about the time of sunrise and sunset"""
    # wthr = get_weather(get_coordinates())
    return f'Мое сообщение'