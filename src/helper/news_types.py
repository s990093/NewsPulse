from typing import TypedDict, List

class NewsItem(TypedDict):
    id: str
    time: str
    title: str
    content: str
    url: str
    domain: str

NewsList = List[NewsItem]
