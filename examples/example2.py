
import asyncio

from examples.settings import settings
from src.weather_api_sdk import WeatherAPISDK


async def main() -> None:
    async with WeatherAPISDK(settings.OPENWEATHERMAP_API_KEY, mode='polling_mode') as weather_sdk:
        city_info = await weather_sdk.get_weather_by_city('Almaty')
        print(city_info)

        city_info = await weather_sdk.get_weather_by_city('Pavlodar')
        print(city_info)

        print('⏳ Waiting to observe polling...')
        await asyncio.sleep(900)

        city_info = await weather_sdk.get_weather_by_city('Pavlodar')
        print(city_info)


if __name__ == '__main__':
    asyncio.run(main())