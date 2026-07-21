import requests
from django.shortcuts import render

def home(request):
    city = request.GET.get('city')

    if city:
        api_key = "26f65745b9b4e4297fd332d667034e31"   # 👉 put your API key

        # CURRENT WEATHER
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()

        if str(res.get("cod")) != "200":
            return render(request, 'index.html', {
                'error': "City not found"
            })

        # FORECAST (5 entries)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        forecast_res = requests.get(forecast_url).json()

        forecast_data = []
        for i in forecast_res['list'][0:5]:
            forecast_data.append({
                'temp': i['main']['temp'],
                'icon': i['weather'][0]['icon'],
                'time': i['dt_txt']
            })

        data = {
            'city': city,
            'temperature': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'humidity': res['main']['humidity'],
            'wind': res['wind']['speed'],
            'feels': res['main']['feels_like'],
            'icon': res['weather'][0]['icon']
        }

        return render(request, 'index.html', {
            'data': data,
            'forecast': forecast_data
        })

    return render(request, 'index.html')