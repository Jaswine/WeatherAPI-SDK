
import asyncio
import logging

from requests import Response, get, RequestException

from src.cache import Cache
from src.shemas.weather_schemas import WeatherResponseSchema, WeatherForWeatherResponseSchema, \
    TemperatureForWeatherResponseSchema, WindForWeatherResponseSchema, SysForWeatherResponseSchema

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

class Modes:
    ON_DEMAND = "on_demand"
    POLLING_MODE = "polling_mode"

class WeatherAPISDK:
    __api_url = 'https://api.openweathermap.org/data/2.5'
    __used_keys = set()

    def __init__(self, api_key: str,  mode=Modes.ON_DEMAND):
        if api_key in self.__used_keys:
            raise ValueError('SDK with key', api_key, 'already exists')

        self.api_key = api_key
        WeatherAPISDK.__used_keys.add(api_key)

        self.cache = Cache(limit=10, ttl_seconds=600)
        self.mode = mode
        self.refresh_interval = 600     # 10 minutes
        self._polling_task = None

        if mode == Modes.POLLING_MODE:
            self._polling_task = asyncio.create_task(self._background_refresh())


    def __fetch_data(self, city_name: str) -> Response:
        """
            Fetch data

            :param request: Request
            :return: Response
        """
        url = f'{self.__api_url}/weather?q={city_name}&appid={self.api_key}'

        try:
            response = get(url, timeout=10)
        except RequestException as e:
            raise ConnectionError(f"Failed to connect to weather API: {e}")

        if response.status_code != 200:
            try:
                error_message = response.json().get("message", "Unknown error")
            except Exception:
                error_message = response.text or "Unknown error"

            raise ValueError(f"API error {response.status_code}: {error_message}")

        return response

    def get_weather_by_city(self, city_name: str) -> WeatherResponseSchema:
        """
            Return information about the weather at the current moment.

            :param city_name: str - City's name
            :return: str - information about weather
        """
        # Get weather cached data
        cached = self.cache.get(city_name)
        if cached:
            logger.info(f"⚡ Using cached data for {city_name}")
            return cached.model_dump()

        # Fetching weather data
        logger.info(f"🌐 Fetching weather data for {city_name} from API")
        response = self.__fetch_data(city_name)
        data = response.json()

        weather_data = WeatherResponseSchema(
            weather=WeatherForWeatherResponseSchema(
                main=data.get("weather", [])[0].get("main"),
                description=data.get("weather", [])[0].get("description"),
            ), temperature=TemperatureForWeatherResponseSchema(
                temp=data.get("main", {}).get("temp", 0.0),
                feels_like=data.get("main", {}).get("feels_like", 0.0)
            ), visibility=data.get("visibility", 0),
            wind=WindForWeatherResponseSchema(
                speed=data.get("wind", {}).get("speed", 0)
            ), datetime=data.get("dt", 0),
            sys=SysForWeatherResponseSchema(
                sunrise=data.get("sys", {}).get("sunrise", 0),
                sunset=data.get("sys", {}).get("sunset", 0),
            ), timezone=data.get("timezone", 0),
            name=data.get("name", "")
        )

        # Add weather data to cache
        self.cache.add(city_name, weather_data)
        logger.info(f"✅ Cached weather data for {city_name}")

        return weather_data.model_dump()


    async def _background_refresh(self) -> None:
        """
            SDK requests new weather information for all stored locations
        """
        while True:
            for city_name in list(self.cache.keys()):
                logger.info(f"🔁 Update cache for {city_name}")
                self.get_weather_by_city(city_name)
            await asyncio.sleep(self.refresh_interval)

    def stop_polling(self) -> None:
        """
            Stop polling
        """
        if self._polling_task:
            self._polling_task.cancel()
            logger.info("🛑 Polling stopped")

    def delete(self) -> None:
        """
           Manually delete the SDK instance and stop background tasks.
        """
        logger.info("🗑️ Deleting WeatherAPISDK instance...")

        self.stop_polling()

        WeatherAPISDK.__used_keys.discard(self.api_key)

        self.cache.clear()

        self._polling_task = None

        logger.info("✅ Weather API SDK instance deleted successfully!")

    def __del__(self) -> None:
        self.delete()



