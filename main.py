from src.gpt import analyze_with_gpt
from src.tool import check_economic_terms, load_news
from rich import print
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

news = load_news()

def display_result(title, content, style="bold cyan"):
    """用于以格式化面板显示结果的工具函数。"""
    panel_title = f"[{style}]{title}[/{style}]"
    return Panel(Text(content), title=panel_title)

if __name__ == "__main__":
    # 新闻内容
    news_content = news
    
    print(check_economic_terms(news_content))
    
    
    # # 1. 新闻分类
    # classification_prompt = "你是一个新闻分类器。将以下新闻分类为财经或政治。"
    # classification_result = analyze_with_gpt(news_content, classification_prompt)
    # classification_panel = display_result("新闻分类", classification_result)
    
    # # 2. 关键词提取
    # keyword_prompt = "你是一个关键词提取器。从文章中提取主要关键词。"
    # keywords_result = analyze_with_gpt(news_content, keyword_prompt)
    # keywords_panel = display_result("关键词", keywords_result)
    
    # # 3. 摘要生成
    # summary_prompt = "你是一个摘要生成器。将以下文章总结为2-3句话。"
    # summary_result = analyze_with_gpt(news_content, summary_prompt)
    # summary_panel = display_result("摘要", summary_result)
    
    # # 4. 情感分析
    # sentiment_prompt = "你是一个情感分析器。分析新闻文章的情感，判断为积极、消极或中立。"
    # sentiment_result = analyze_with_gpt(news_content, sentiment_prompt)
    # sentiment_panel = display_result("情感分析", sentiment_result)
    
    # # 并排显示分类、关键词、摘要和情感分析
    # print(Columns([classification_panel, keywords_panel, summary_panel, sentiment_panel]))
    
    # # 5. 跨领域影响分析（仅当分类为政治时）
    # if "政治" in classification_result.lower():
    #     cross_impact_prompt = "你是一个跨领域影响分析器。分析政治新闻对金融领域的影响。"
    #     cross_impact_result = analyze_with_gpt(news_content, cross_impact_prompt)
    #     cross_impact_panel = display_result("跨领域影响（政治对金融）", cross_impact_result)
    #     print(cross_impact_panel)
    
    # # 6. 趋势预测
    # trend_prompt = "你是一个趋势预测器。根据这篇新闻文章预测长期趋势。"
    # trend_result = analyze_with_gpt(news_content, trend_prompt)
    # trend_panel = display_result("趋势预测", trend_result)
    # print(trend_panel)
