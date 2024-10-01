from rich.console import Console
from rich.progress import Progress
from src.news import load_news
from src.gpt import analyze_news

console = Console()

if __name__ == "__main__":
    json_file_path = 'data/news.json'
    news_data = load_news(json_file_path)
       
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing news...", total=len(news_data))

        for news in news_data:
            analyze_news(news)
            progress.update(task, advance=1)  
    console.print("[green]All news articles have been analyzed![/green]")
