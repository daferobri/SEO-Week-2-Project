from dotenv import load_dotenv
import os
import resend
from gen_ai import get_email_html

load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]

def send_email(address, events):
    html = get_email_html(events)

    params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": [address],
    "subject": "Events Near You",
    "html": html
    }

    email = resend.Emails.send(params)
    print(email)
