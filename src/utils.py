import re
from bs4 import BeautifulSoup

def strip_html(text: str) -> str:
    if not isinstance(text, str): 
        return ""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(" ", strip=True)

def clean_text_basic(text: str) -> str:
    text = strip_html(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
