from examples.settings import settings
from src.weather_api_sdk import WeatherAPISDK

async def main() -> None:
    weather_sdk = WeatherAPISDK(settings.OPENWEATHERMAP_API_KEY)

    city_info = await weather_sdk.get_weather_by_city('Almaty')

    city_info = await weather_sdk.get_weather_by_city('Almaty')

    city_info = await weather_sdk.get_weather_by_city('Almaty')
    print(city_info)

    city_info = await weather_sdk.get_weather_by_city('Pavlodar')
    print(city_info)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())