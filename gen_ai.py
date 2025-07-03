import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
my_api_key = os.getenv('GENAI_KEY')

genai.configure(api_key=my_api_key)


def get_email_html(contents):
    response = genai.GenerativeModel(
        "gemini-1.5-flash").generate_content(contents)
    markdown_match = re.search(
        r"```html\s*(.*?)\s*```",
        response.text,
        re.DOTALL | re.IGNORECASE
    )
    if markdown_match:
        html_code = markdown_match.group(1).strip()
        return html_code

    match = re.search(
        r"<!DOCTYPE html>.*?</html>",
        response.text,
        re.DOTALL | re.IGNORECASE
    )
    if match:
        html_code = match.group(0)
        # print(html_code)
        return html_code
    else:
        return "Error"
