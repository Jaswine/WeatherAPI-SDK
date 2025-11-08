
import asyncio
import logging

from aiohttp import ClientSession, ClientError, ClientResponse

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
        self.refresh_interval = 30     # 600  # 10 minutes
        self._polling_task = None
        self._session: ClientSession | None = None

    async def __aenter__(self):
        """
            Context manager support
        """
        self._session = ClientSession()
        if self.mode == Modes.POLLING_MODE:
            self._polling_task = asyncio.create_task(self._background_refresh())
            logger.info("🌀 Polling mode enabled: background refresh started")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.delete()

    async def __fetch_data(self, city_name: str) -> ClientResponse:
        """
            Fetch data

            :param city_name: str - City name
            :return: ClientResponse - Information about weather
        """
        if not self._session:
            self._session = ClientSession()

        url = f'{self.__api_url}/weather?q={city_name}&appid={self.api_key}'

        try:
            async with self._session.get(url, timeout=10) as response:
                data = await response.json()
                if response.status != 200:
                    error_message = data.get("message", "Unknown error")
                    raise ValueError(f"API error {response.status}: {error_message}")
                return data
        except ClientError as e:
            raise ConnectionError(f"Failed to connect to weather API: {e}")

    async def get_weather_by_city(self, city_name: str) -> WeatherResponseSchema:
        """
            Return information about the weather at the current moment.

            :param city_name: str - City name
            :return: str - Information about weather
        """
        # Get weather cached data
        cached = self.cache.get(city_name)
        if cached:
            logger.info(f"⚡ Using cached data for {city_name}")
            return cached.model_dump()

        # Fetching weather data
        logger.info(f"🌐 Fetching weather data for {city_name} from API")
        data = await self.__fetch_data(city_name)

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
        try:
            while True:
                for city_name in list(self.cache.keys()):
                    logger.info(f"🔁 Update cache for {city_name}")
                    await self.get_weather_by_city(city_name)
                logger.info("💤 Sleeping until next update...")
                await asyncio.sleep(self.refresh_interval)
        except asyncio.CancelledError:
            logger.info("🛑 Polling task cancelled")

    async def stop_polling(self) -> None:
        """
            Stop polling task
        """
        if self._polling_task:
            self._polling_task.cancel()
            logger.info("🛑 Polling stopped")

    async def delete(self) -> None:
        """
           Manually delete the SDK instance and stop background tasks.
        """
        logger.info("🗑️ Deleting WeatherAPISDK instance...")

        await self.stop_polling()

        WeatherAPISDK.__used_keys.discard(self.api_key)
        self.cache.clear()

        if self._session:
            await self._session.close()

        self._polling_task = None
        self._session = None

        logger.info("✅ Weather API SDK instance deleted successfully!")

    def __del__(self) -> None:
        try:
            if self._session and not self._session.closed:
                try:
                    asyncio.create_task(self._session.close())
                except RuntimeError:
                    pass

            try:
                if self._polling_task:
                    self._polling_task.cancel()
            except Exception:
                pass

            WeatherAPISDK.__used_keys.discard(self.api_key)
            self.cache.clear()
        except Exception:
            pass



