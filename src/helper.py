import re
from langdetect import detect, LangDetectException

def preprocess_content(content):
    # 去除不必要的空白字符
    content = content.strip()

    # 去除多余的空行
    content = re.sub(r'\n\s*\n', '\n', content)

    # 去除前后多余的空格
    content = re.sub(r'\s+', ' ', content)

    # 去除重复的段落（按行比较）
    seen = set()
    unique_lines = []
    for line in content.split('\n'):
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            unique_lines.append(line)

    # 重新组合内容
    processed_content = '\n'.join(unique_lines)

    return processed_content




def clean_string(input_string):
    """
    去除字符串中的空格和引號。
    
    參數:
    input_string (str): 要處理的字符串。
    
    返回:
    str: 處理後的字符串。
    """
    # 去除空格和引號
    cleaned_string = input_string.replace('"', '').replace(' ', '')
    return cleaned_string



def preprocess_content(content):
    """
    清除不必要的標點符號和多餘的空格。
    
    參數:
        content (str): 需要預處理的文本內容。
        
    返回:
    
        str: 處理後的內容。
    """
    # 移除所有不必要的標點符號，只保留文字和空格
    content = re.sub(r'[^\w\s]', '', content)  # 移除標點符號
    # 將多餘的空格替換為單一空格
    content = re.sub(r'\s+', ' ', content).strip()  # 去掉多餘空格
    return content



def detect_language(text):
    """
    檢測文本的語言。

    參數:
        text (str): 需要檢測語言的文本。

    返回:
        str: 檢測到的語言代碼（例如 'en', 'zh'）。
    """
    try:
        return detect(text)
    except LangDetectException:
        print("無法檢測語言，文本可能太短或不清晰。")
        return None