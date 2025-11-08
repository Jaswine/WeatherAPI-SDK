
# Weather API SDK

## 📋 Description

**Task**: Develop a SDK for accessing a weather API ( https://openweathermap.org/api )

**Objective**: The objective of this task is to develop a software development kit (SDK) that can be used by
other developers to easily access a weather API and retrieve weather data for a given location.

**Tech Stack:**
- Python 3.11+
- asyncio / aiohttp
- pydantic

## 🚀 Quick Start

### Local Development (Recommended)

#### 1. Prerequisites

- Python 3.11+

#### 2. Install Dependencies

```bash
# Create virtual environment
make setup

# Install project dependencies
make install
```

#### 3. Configure Environment Variables

Create `.env` file and get api key from https://home.openweathermap.org/api_keys:

```bash
cp .env.example .env
```

#### 4. Run examples

```bash
make run
```

## 📂 Project Structure

```
weatherapi-sdk/
├── examples/
│   ├── example1.py         # Example 1
│   ├── example2.py         # Example 2
│   └── settings.py         # Settings for examples
├── src/
│   ├── shemas/             # Schemas
│   │   └── weather_schemas.py
│   ├── cache.py            # Cache
│   └── weather_api_sdk.py  # SDK
├── Makefile
├── README.md
└── requirements.txt
```

## 🛠️ Available Commands

All commands are executed via `make`:

- `make setup` — create virtual environment
- `make install` — install dependencies from requirements.txt
- `make run` - run all examples

## 🔧 Configuration

#### Required Variables

| Variable | Description                                            | Example | 
|----------|--------------------------------------------------------|---------|
| `OPENWEATHERMAP_API_KEY` | Api key from https://home.openweathermap.org/api_keys  | `12345` |


## 📚 Documentation

### `get_weather_by_city(city_name: str) -> dict`

Returns weather information for the specified city.

**Parameters:**

- `city_name` (`str`): City name, for example `"Almaty"`.

**Returns:**

- `dict`: JSON-like dictionary with weather data:
  ```json
  {
      "weather": {"main": "Clouds", "description": "scattered clouds"},
      "temperature": {"temp": 269.6, "feels_like": 267.57},
      "visibility": 10000,
      "wind": {"speed": 1.38},
      "datetime": 1675744800,
      "sys": {"sunrise": 1675751262, "sunset": 1675787560},
      "timezone": 3600,
      "name": "Zocca"
  }
  
**Exceptions:**
    `ValueError` - if the API returned an error
    `ConnectionError` - if it was not possible to connect to the API

**Example:**
```python
from src.weather_api_sdk import WeatherAPISDK, WeatherAPISDK_Modes

async def main():
    async with WeatherAPISDK("YOUR_API_KEY", mode=WeatherAPISDK_Modes.ON_DEMAND) as sdk:
        weather = await sdk.get_weather_by_city("Almaty")
        print(weather)
```

## 💡 Issues and Support

If you encounter problems:
1. Check logs
2. Check environment variables in `.env`
3. Create issue in GitHub
