import requests
from datetime import datetime

cities = {
    "Россия": {
        "Москва": {"lat": 55.76, "lon": 37.62},
        "Санкт-Петербург": {"lat": 59.93, "lon": 30.36},
        "Новосибирск": {"lat": 55.01, "lon": 82.94},
        "Екатеринбург": {"lat": 56.84, "lon": 60.61},
        "Казань": {"lat": 55.79, "lon": 49.13}
    },
    "Казахстан": {
        "Астана": {"lat": 51.16, "lon": 71.47},
        "Алматы": {"lat": 43.24, "lon": 76.89},
        "Шымкент": {"lat": 42.34, "lon": 69.59},
        "Караганда": {"lat": 49.80, "lon": 73.10},
        "Актобе": {"lat": 50.28, "lon": 57.17}
    },
    "Кыргызстан": {
        "Бишкек": {"lat": 42.87, "lon": 74.57},
        "Ош": {"lat": 40.53, "lon": 72.80},
        "Джалал-Абад": {"lat": 40.93, "lon": 73.00},
        "Каракол": {"lat": 42.49, "lon": 78.39},
        "Талас": {"lat": 42.52, "lon": 72.24}
    }
}

# Пользовательский ввод
user_country = input('Выбери страну (Россия, Казахстан, Кыргызстан): ')

if user_country not in cities.keys():
    print('Вы ввели неверное название страны или ее нет в списке.')
    exit()

user_city = input(f'Выбери город из списка {list(cities[user_country].keys())}: ')

latitude = cities[user_country][user_city]['lat']
longitude = cities[user_country][user_city]['lon']

# Запрос к Open-Meteo
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    "&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,surface_pressure,apparent_temperature,visibility"
    "&timezone=auto"
)

response = requests.get(url)
data = response.json()

# Получаем текущий час в нужном формате
current_time = datetime.now().strftime('%Y-%m-%dT%H:00')

# Находим индекс текущего времени
times = data['hourly']['time']
index = times.index(current_time)


# Получаем погоду
temperature = data['hourly']['temperature_2m'][index]
wind_speed = data['hourly']['windspeed_10m'][index]
humidity = data['hourly']['relativehumidity_2m'][index]
pressure = data['hourly']['surface_pressure'][index]
apparent_temperature = data['hourly']['apparent_temperature'][index]
visibility = data['hourly']['visibility'][index]



# Вывод
print(f"Погода в городе {user_city} на {current_time}:")
print(f"🌡 Температура: {temperature}°C")
print(f"🌡 Ощущается как: {apparent_temperature}°C")
print(f"💨 Скорость ветра: {wind_speed} м/с")
print(f"💧 Влажность: {humidity}%")
print(f'Давление: {pressure} гПа')
print(f'🌫️ Видимость: {visibility / 1000} м')
