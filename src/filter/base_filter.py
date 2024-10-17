import re
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
from abc import ABC, abstractmethod
from rich.progress import Progress
from rich.console import Console

from src.helper.news_types import NewsList
class NewsAnalysisBase(ABC):
    """
    抽象基類，定義新聞分析的基本結構和流程
    """

    @abstractmethod
    def filter_news(self, news_data: NewsList, *args, **kwargs) -> NewsList:
        """
        過濾符合條件的新聞
        """
        pass

    @abstractmethod
    def analyze_news(self, news_data, *args, **kwargs):
        """
        分析過濾後的新聞，統計相關數據
        """
        pass

    @abstractmethod
    def generate_charts(self, analysis_data, *args, **kwargs):
        """
        根據分析結果生成圖表
        """
        pass

