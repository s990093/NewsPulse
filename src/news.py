import json
import os
from typing import Dict, Any

class NewsArticle:
    def __init__(self, data: Dict[str, Any]):
        self.id = data['id']
        self.type = data['type']
        self.source = data['source']
        self.title = data['title']
        self.date = data['date']
        # self.preprocessed_news = data['preprocessed_news']

    def get_content(self) -> str:
        """Get the content of the news article from the corresponding text file."""
        content_file_path = f"data/content/{self.id}.txt"
        if os.path.exists(content_file_path):
            with open(content_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return f"No content file found for news ID: {self.id}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the NewsArticle object to a dictionary."""
        return {
            'id': self.id,
            'type': self.type,
            'source': self.source,
            'title': self.title,
            'date': self.date,
            # 'preprocessed_news': self.preprocessed_news
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NewsArticle':
        """Create a NewsArticle object from a dictionary."""
        return cls(data)
def load_news(json_file_path):
    """Load news from the JSON file and return a list of NewsArticle objects."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            news_data = json.load(file)
            return [NewsArticle(news) for news in news_data]
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON")
        return []