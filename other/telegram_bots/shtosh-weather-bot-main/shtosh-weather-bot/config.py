BOT_API_TOKEN = '6128619632:AAF0evAyz2QPtFLdbhLSpSZRGV1MVHrL7gA'
WEATHER_API_KEY = '06db8cad325cc9211afd52df8b6fc223'

CURRENT_WEATHER_API_CALL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={latitude}&lon={longitude}&'
        'appid=' + WEATHER_API_KEY + '&units=metric'
)
