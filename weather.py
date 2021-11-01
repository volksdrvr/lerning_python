import requests

def get_weather_desc_and_temp():
    api_key = "42b0d5523bd4abb83a92a181dc1fd95b"
    city = "Amsterdam"
    url = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key+"&units=imperial"

    request = requests.get(url)
    json = request.json()
    # print(json)

    description = json.get("weather")[0].get("description")
    temp_max = json.get("main").get("temp_max")
    temp_min = json.get("main").get("temp_min")

    return {
        'description': description,
        'temp_max': temp_max,
        'temp_min': temp_min
        }

def main():
    weather_dict = get_weather_desc_and_temp()
    print("Today's forcast is:", weather_dict.get('description'))
    print("The minimum tempature is:", weather_dict.get('temp_min'))
    print("The maximum tempature is:", weather_dict.get('temp_max'))

main()