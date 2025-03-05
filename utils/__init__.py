# This file makes the utils directory a Python package
# It allows importing modules from the utils directory

from utils.weather import WeatherService
from utils.news import NewsService

__all__ = ['WeatherService', 'NewsService']