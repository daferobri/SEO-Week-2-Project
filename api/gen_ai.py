import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
my_api_key = os.getenv('GENAI_KEY')

genai.api_key = my_api_key

client = genai.Client(
    api_key=my_api_key,
)

def get_email_html(contents):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="Rewrite the contents into visually appealing HTML for an email, and do not write anything but HTML code."
        ),
        contents=contents,
    )

    match = re.search(r"<!DOCTYPE html>.*?</html>", response.text, re.DOTALL | re.IGNORECASE)
    if match:
        html_code = match.group(0)
        # print(html_code)
        return html_code
    else:
        return "Error"

get_email_html("")