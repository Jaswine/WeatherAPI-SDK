from src.weather_api_sdk import WeatherAPISDK


def main() -> None:
    API_KEY = '18ee8e1c90d7b8f7004afc7b52946a37'

    weather_sdk = WeatherAPISDK(API_KEY)
    city_info = weather_sdk.get_weather_by_city('Almaty')

    city_info = weather_sdk.get_weather_by_city('Almaty')
    print(city_info)

    city_info = weather_sdk.get_weather_by_city('Pavlodar')
    print(city_info)

    weather_sdk = WeatherAPISDK(API_KEY)

    print(city_info)

if __name__ == '__main__':
    main()