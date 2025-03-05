import re
import logging
import random
from typing import Dict, List, Optional, Any
from pathlib import Path

# Setup logger
logger = logging.getLogger(__name__)

class NewsService:
    """Service for handling news data and processing."""
    
    def __init__(self, news_file_path: str):
        """
        Initialize the news service.
        
        Args:
            news_file_path: Path to the news data file
        """
        self.news_file_path = news_file_path
        
    def _ensure_file_exists(self) -> bool:
        """
        Ensure the news file exists.
        
        Returns:
            True if the file exists or was created, False otherwise
        """
        try:
            Path(self.news_file_path).touch(exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating news file: {str(e)}")
            return False
    
    def read_news_file(self) -> str:
        """
        Read the content of the news file.
        
        Returns:
            Content of the news file as a string
        """
        try:
            self._ensure_file_exists()
            
            with open(self.news_file_path, "r", encoding="utf-8") as file:
                data = file.read()
                
            return data
        except Exception as e:
            logger.error(f"Error reading news file: {str(e)}")
            return ""
    
    def parse_news_entries(self, data: str) -> List[Dict[str, str]]:
        """
        Parse news entries from raw data.
        
        Args:
            data: Raw news data as a string
            
        Returns:
            List of news entry dictionaries with title, description, and date
        """
        try:
            entries = []
            
            # Split the data into individual news entries
            # Assuming each entry starts with "Title: "
            raw_entries = re.split(r"(?=Title: )", data)
            
            # Remove any empty entries
            raw_entries = [entry for entry in raw_entries if entry.strip()]
            
            for entry in raw_entries:
                try:
                    # Extract title, description, and date
                    title_match = re.search(r"Title: (.*?)(?=$|\n)", entry)
                    description_match = re.search(r"Description: (.*?)(?=$|\n)", entry)
                    date_match = re.search(r"Date: (.*?)(?=$|\n)", entry)
                    
                    if title_match and description_match and date_match:
                        news_entry = {
                            "title": title_match.group(1).strip(),
                            "description": description_match.group(1).strip(),
                            "date": date_match.group(1).strip()
                        }
                        entries.append(news_entry)
                except Exception as e:
                    logger.warning(f"Error parsing news entry: {str(e)}")
                    continue
                    
            logger.info(f"Parsed {len(entries)} news entries")
            return entries
            
        except Exception as e:
            logger.error(f"Error parsing news data: {str(e)}")
            return []
    
    def get_random_happy_news(self) -> Optional[Dict[str, str]]:
        """
        Get a random happy news entry.
        
        Returns:
            Random news entry or None if no entries available
        """
        try:
            # Read and parse the news file
            data = self.read_news_file()
            
            if not data:
                logger.warning("No news data available")
                return None
                
            entries = self.parse_news_entries(data)
            
            if not entries:
                logger.warning("No valid news entries found")
                return None
                
            # Select a random entry
            random_entry = random.choice(entries)
            
            logger.info(f"Selected random news entry: {random_entry['title']}")
            return random_entry
            
        except Exception as e:
            logger.error(f"Error getting random news: {str(e)}")
            return None
    
    def get_first_news_entry(self) -> Optional[Dict[str, str]]:
        """
        Get the first news entry from the file.
        
        Returns:
            First news entry or None if no entries available
        """
        try:
            # Read and parse the news file
            data = self.read_news_file()
            
            if not data:
                logger.warning("No news data available")
                return None
                
            entries = self.parse_news_entries(data)
            
            if not entries:
                logger.warning("No valid news entries found")
                return None
                
            # Return the first entry
            logger.info(f"Retrieved first news entry: {entries[0]['title']}")
            return entries[0]
            
        except Exception as e:
            logger.error(f"Error getting first news entry: {str(e)}")
            return None