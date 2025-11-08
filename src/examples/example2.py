
import asyncio

from src.weather_api_sdk import WeatherAPISDK


async def main() -> None:
    API_KEY = ''

    async with WeatherAPISDK(API_KEY, mode="polling_mode") as weather_sdk:
        city_info = await weather_sdk.get_weather_by_city('Almaty')
        print(city_info)

        city_info = await weather_sdk.get_weather_by_city('Pavlodar')
        print(city_info)

        print("⏳ Waiting to observe polling...")
        await asyncio.sleep(100) # 900

        city_info = await weather_sdk.get_weather_by_city('Pavlodar')
        print(city_info)


if __name__ == '__main__':
    asyncio.run(main())