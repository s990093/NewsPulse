from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from rich.console import Console
from rich.progress import Progress
from src.analyze import process_cluster
from src.news import load_news
from src.gpt import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

console = Console()

if __name__ == "__main__":
    # # Load existing results if available
    # try:
    #     existing_results_df = pd.read_csv('news_analysis_results.csv')
    #     existing_ids = set(existing_results_df['ID'].astype(int))  # Convert IDs to a set for fast lookup
    # except FileNotFoundError:
    #     existing_ids = set()  # If the file does not exist, process all IDs

    # Read new news data
    df = pd.read_csv('data/csv/data.csv')

    # Remove duplicates and keep the first occurrence
    df = df.drop_duplicates(subset='id', keep='first')

    # Filter out news articles that have already been processed
    # new_news_df = df[~df['id'].isin(existing_ids)][:1]
    
    new_news_df = df
    
    # console.print("使用比率", len(new_news_df)/len(df['id']))

    results = []
    total_news = len(new_news_df)
    success_count = 0
    failure_count = 0
    max_workers = 10

    # Set up ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(analyze_news_v0, news["id"], news["content"], news["title"]): index for index, news in new_news_df.iterrows()}

        for future in as_completed(futures):
            index = futures[future]
            try:
                news_id, relation_ratio, sentiment_ratio, country, elapsed_time = future.result()

                if news_id is not None:
                    # Add successful analysis results to results
                    # results.append({
                    #     "id": news_id,  # Include the news_id for reference
                    #     "relation_ratio": relation_ratio, 
                    #     "sentiment_ratio": sentiment_ratio, 
                    #     "country": country, 
                    #     "analysis_time": elapsed_time
                    # })
                    success_count += 1
                else:
                    failure_count += 1
            except TypeError:
                    # console.print(f"Analysis failed for index {index}: No valid result returned.")
                    failure_count += 1
            except Exception as e:
                console.print(f"新聞分析失敗，index {index}，錯誤: {e}")
                console.print(traceback.format_exc())  # Print the traceback

                failure_count += 1

            # Update processing progress
            console.print(f"Processing news {index + 1}/{total_news} - 成功: {success_count}, 失敗: {failure_count}")

    # Final success and failure ratio
    success_ratio = success_count / total_news if total_news > 0 else 0
    failure_ratio = failure_count / total_news if total_news > 0 else 0
    console.print(f"分析完成。成功比例: {success_ratio:.2%}, 失敗比例: {failure_ratio:.2%}")

    # Create DataFrame and save results to CSV file
    if results:
        results_df = pd.DataFrame(results)
        # results_df.to_csv('news_analysis_results.csv', mode='a', index=False, header=not existing_ids)  # Append to the existing CSV
    else:
        console.print("無法保存結果，沒有成功的分析。")
