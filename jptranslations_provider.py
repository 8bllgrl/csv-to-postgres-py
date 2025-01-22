import re

def clean_text(text):
    if isinstance(text, str):
        return text.replace("（★未使用／削除予定★）", "")
    return text


def is_japanese(text):
    if isinstance(text, str):
        cleaned_text = clean_text(text)
        japanese_pattern = re.compile('[\u3040-\u30FF\u4E00-\u9FFF]')
        return bool(japanese_pattern.search(cleaned_text))
    return False
