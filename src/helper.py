import re

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