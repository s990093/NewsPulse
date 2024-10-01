import random
import openai

from src.helper import clean_string, preprocess_content
from src.tool import analyze_sentiment_ratio, export_to_csv
from src.news import NewsArticle

# optional; defaults to `os.environ['OPENAI_API_KEY']


api_keys = ["sk-JsX1k5W4cJmkII0F005273A2E4D1430eBf1bB38a92Dc33Fb",
       "sk-ouapzZyTJaNSUAO480744a8693F446B1B1A552Da73A05971" ]

openai.base_url = "https://free.gpt.ge/v1/"
openai.default_headers = {"x-foo": "true"}


def analyze_with_gpt(content, task_prompt, model="gpt-3.5-turbo-0125", temperature=0, max_tokens=200, top_p=1, frequency_penalty=0.0, presence_penalty=0.0):
    openai.api_key = random.choice(api_keys)

    try:
        completion = openai.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            messages=[
                {"role": "system", "content": task_prompt},
                {"role": "user", "content": content}
            ]
        )
        return completion.choices[0].message.content
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "Error in generating response"


def analyze_news(news: NewsArticle):
    news_content = preprocess_content(news.get_content())

    summary_prompt = "提取關於新聞的重要資訊，移除無關內容，簡短、直接，用最少字數表達，100個字以內。"
    summary_report = clean_string(analyze_with_gpt(news_content, summary_prompt))
    
    
    title_prompt = "提取內文給一個標題，移除無關內容，簡短、直接"
    title = clean_string(analyze_with_gpt(summary_report, title_prompt))
    
    print(news.id, title)
    
    # 定義用於從新聞中提取重要資訊的提示
    news_extraction_prompt = "幫我根據內容做出這篇文章的7個關鍵字名詞，一行字串用/分隔，不准使用其他格式與換行，不可以講新聞報導/新聞/財經大範圍等主題"
    while True:
        # 使用GPT進行分析
        extracted_news_info = analyze_with_gpt(summary_report, news_extraction_prompt)

        if extracted_news_info and "/" in extracted_news_info and "\n" :
            # print("提取的新聞資訊：", extracted_news_info)
            break  # 如果有效，退出循環
        else:
            print("未能提取有效的新聞資訊，請重試。")
            # 根據需要可以在這裡修改 summary_report 或重置 extracted_news_info
            
            

    # 計算字數
    original_word_count = len(news_content.split())
    summary_word_count = len(summary_report.split())

    # 計算縮小比
    compression_ratio = original_word_count / summary_word_count if summary_word_count > 0 else float('inf')

    # 第二步：進行情感分析
    sentiment_prompt = "針對以下新聞內容進行情感分析，簡短直接，移除多餘內容。"
    sentiment_result = clean_string(analyze_with_gpt(summary_report, sentiment_prompt))
    sentiment_ratio = analyze_sentiment_ratio(sentiment_result)

    # 第三步：進行簡易趨勢分析
    trend_analysis_prompt = "提供簡短的趨勢分析，去除無關內容，重點簡述趨勢。"
    trend_result = clean_string(analyze_with_gpt(sentiment_result, trend_analysis_prompt))
    
    
   # 其他參數
    country_analysis_prompt = "並回傳該文章的國家的統一大寫簡寫,簡短直接，移除多餘內容。"
    country = clean_string(analyze_with_gpt(summary_report, country_analysis_prompt))


    # 第四步：匯出結果到 CSV
    export_to_csv(news.id,
                  title,
                  sentiment_result, 
                  sentiment_ratio, 
                  trend_result, 
                  extracted_news_info,
                  summary_report,
                  compression_ratio,
                  country)