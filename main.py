from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
from rich.console import Console
from src.analyze import process_cluster
from src.news import load_news
from src.gpt import analyze_news_v0
import traceback

console = Console()

def load_and_prepare_data(file_path):
    """Load and prepare news data from CSV file."""
    df = pd.read_csv(file_path)
    return df.drop_duplicates(subset='id', keep='first')

def process_single_news(news_data):
    """Process a single news article."""
    try:
        news_id, relation_ratio, sentiment_ratio, country, elapsed_time = analyze_news_v0(
            news_data["id"], 
            news_data["content"], 
            news_data["title"]
        )
        
        if news_id is not None:
            return True, {
                "id": news_id,
                "relation_ratio": relation_ratio,
                "sentiment_ratio": sentiment_ratio,
                "country": country,
                "analysis_time": elapsed_time
            }
    except Exception as e:
        console.print(f"新聞分析失敗，錯誤: {e}")
        console.print(traceback.format_exc())
    
    return False, None

def analyze_news_parallel(news_df, max_workers=10):
    """Analyze multiple news articles in parallel."""
    total_news = len(news_df)
    success_count = failure_count = 0
    results = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_news, news): index 
            for index, news in news_df.iterrows()
        }

        for future in as_completed(futures):
            index = futures[future]
            success, result = future.result()
            
            if success:
                results.append(result)
                success_count += 1
            else:
                failure_count += 1

            console.print(f"Processing news {index + 1}/{total_news} - "
                        f"成功: {success_count}, 失敗: {failure_count}")

    return results, success_count, failure_count

def save_results(results, output_file='news_analysis_results.csv'):
    """Save analysis results to CSV file."""
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_file, index=False)
        return True
    return False

def main():
    # Load and prepare data
    news_df = load_and_prepare_data('data/csv/data.csv')
    
    # Analyze news
    results, success_count, failure_count = analyze_news_parallel(news_df)
    
    # Report results
    total_news = len(news_df)
    success_ratio = success_count / total_news if total_news > 0 else 0
    failure_ratio = failure_count / total_news if total_news > 0 else 0
    console.print(f"分析完成。成功比例: {success_ratio:.2%}, 失敗比例: {failure_ratio:.2%}")
    
    # Save results
    if not save_results(results):
        console.print("無法保存結果，沒有成功的分析。")

if __name__ == "__main__":
    main()

