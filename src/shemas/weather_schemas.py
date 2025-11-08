
from pydantic import BaseModel

class WeatherForWeatherResponseSchema(BaseModel):
    main: str           # Clouds
    description: str    # Scattered clouds

class TemperatureForWeatherResponseSchema(BaseModel):
    temp: float         # 269.6
    feels_like: float   # 267.57

class WindForWeatherResponseSchema(BaseModel):
    speed: float        # 1.38

class SysForWeatherResponseSchema(BaseModel):
    sunrise: int        # 1675751262
    sunset: int         # 1675787560

class WeatherResponseSchema(BaseModel):
    weather: WeatherForWeatherResponseSchema
    temperature: TemperatureForWeatherResponseSchema
    visibility: int     # 10000
    wind:WindForWeatherResponseSchema
    datetime: int       # 1675744800
    sys: SysForWeatherResponseSchema
    timezone: int       # 3600
    name: str           # Zocca