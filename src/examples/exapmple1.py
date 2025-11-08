
from src.weather_api_sdk import WeatherAPISDK


async def main() -> None:
    API_KEY = ''

    weather_sdk = WeatherAPISDK(API_KEY)
    city_info = await weather_sdk.get_weather_by_city('Almaty')

    city_info = await weather_sdk.get_weather_by_city('Almaty')

    city_info = await weather_sdk.get_weather_by_city('Almaty')
    print(city_info)

    city_info = await weather_sdk.get_weather_by_city('Pavlodar')
    print(city_info)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())