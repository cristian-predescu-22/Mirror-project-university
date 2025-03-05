import requests
import logging
from typing import Dict, Any, Optional, Tuple

# Setup logger
logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching and processing weather data."""
    
    def __init__(self, opencage_api_key: str, weather_api_timeout: int = 10):
        """
        Initialize the weather service.
        
        Args:
            opencage_api_key: API key for OpenCage geocoding service
            weather_api_timeout: Timeout for API requests in seconds
        """
        self.opencage_api_key = opencage_api_key
        self.timeout = weather_api_timeout
        
    def get_coordinates(self, city: str, country: str) -> Optional[Tuple[float, float]]:
        """
        Get latitude and longitude coordinates for a location.
        
        Args:
            city: City name
            country: Country name
            
        Returns:
            Tuple of (latitude, longitude) or None if geocoding failed
        """
        try:
            geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={city},+{country}&key={self.opencage_api_key}"
            
            logger.info(f"Fetching coordinates for {city}, {country}")
            geocode_response = requests.get(geocode_url, timeout=self.timeout)
            geocode_data = geocode_response.json()
            
            if not geocode_data.get("results"):
                logger.warning(f"No results found for location: {city}, {country}")
                return None
                
            latitude = geocode_data["results"][0]["geometry"]["lat"]
            longitude = geocode_data["results"][0]["geometry"]["lng"]
            
            logger.info(f"Coordinates found: {latitude}, {longitude}")
            return latitude, longitude
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching coordinates: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing geocoding response: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in geocoding: {str(e)}")
            return None
    
    def get_weather(self, latitude: float, longitude: float, api_key: str, units: str = "metric") -> Optional[Dict[str, Any]]:
        """
        Get weather data for coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            api_key: OpenWeather API key
            units: Units for weather data (metric or imperial)
            
        Returns:
            Weather data dictionary or None if request failed
        """
        try:
            weather_url = (
                f"https://api.openweathermap.org/data/3.0/onecall"
                f"?lat={latitude}&lon={longitude}"
                f"&exclude=minutely,hourly,daily,alerts"
                f"&appid={api_key}&units={units}"
            )
            
            logger.info(f"Fetching weather data for coordinates: {latitude}, {longitude}")
            weather_response = requests.get(weather_url, timeout=self.timeout)
            
            # Check for error responses
            weather_response.raise_for_status()
            
            weather_data = weather_response.json()
            
            # Validate response has expected data
            if 'current' not in weather_data:
                logger.warning("Weather data missing 'current' section")
                return None
                
            logger.info("Weather data retrieved successfully")
            return weather_data
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching weather: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching weather: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"Error parsing weather JSON: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in weather request: {str(e)}")
            return None
    
    def get_weather_for_location(self, city: str, country: str, api_key: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get weather for a specific location.
        
        Args:
            city: City name
            country: Country name
            api_key: OpenWeather API key
            units: Units for weather data
            
        Returns:
            Dictionary with weather data or error status
        """
        # Get coordinates
        coordinates = self.get_coordinates(city, country)
        
        if not coordinates:
            return {"status": "error", "message": "Location not found"}
            
        latitude, longitude = coordinates
        
        # Get weather data
        weather_data = self.get_weather(latitude, longitude, api_key, units)
        
        if not weather_data:
            return {"status": "error", "message": "Weather data not available"}
            
        return weather_data