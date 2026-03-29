"""
internet_engine.py
Handles web integrations: DuckDuckGo scraping, REST API queries (Weather).
"""

import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger()

class InternetEngine:
    def __init__(self):
        self.weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY") or os.getenv("OPENWEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")
        self.news_api_key = os.getenv("NEWS_API_KEY")
        logger.info("Internet engine connected.")

    async def fetch_page(self, url: str) -> str:
        """Fetches a URL and returns clean text using BeautifulSoup."""
        logger.info(f"Fetching URL: {url}")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    text = ' '.join(soup.stripped_strings)
                    return text[:5000] # Truncate to save context
            except Exception as e:
                logger.error(f"Failed fetching {url}: {e}")
                return "Failed to retrieve page content."

    async def get_weather(self, city: str) -> str:
        """Queries OpenWeatherMap for the current weather."""
        if not self.weather_api_key or self.weather_api_key == "your_openweathermap_api_key_here":
            return f"I require a valid OpenWeatherMap API key to check the weather in {city}, sir."
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=5) as response:
                    data = await response.json()
                    if data.get("cod") == 200:
                        temp = data["main"]["temp"]
                        desc = data["weather"][0]["description"]
                        return f"It is currently {temp}°C with {desc} in {city}."
                    else:
                        return f"I could not retrieve the weather data for {city}."
            except Exception as e:
                logger.error(f"Weather API error: {e}")
                return "The weather service is not responding, sir."

    async def perform_search(self, query: str) -> str:
        """Scrapes basic DuckDuckGo HTML search results."""
        logger.info(f"Performing web search for: {query}")
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    results = soup.find_all('a', class_='result__snippet')
                    if results:
                        return results[0].text.strip()
                    return "No results found, sir."
            except Exception as e:
                logger.error(f"Search failed for {query}: {e}")
                return "I could not complete the search at this time."

if __name__ == "__main__":
    async def test():
        ie = InternetEngine()
        print("Test Search Result:", await ie.perform_search("JARVIS MCU"))
    asyncio.run(test())
