from dotenv import load_dotenv
import os
import resend
from gen_ai import get_email_html

load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]


def send_email(address, events):
    prompt = f"""
    Generate an HTML email about upcoming events. here are the event details:
    {events}
    Please create a nicely formatted HTML email with these events, include proper styling and structure
    """
    html = get_email_html(prompt)

    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["daferobri5941@gmail.com"],
        "subject": "Events Near You",
        "html": html
    }

    email = resend.Emails.send(params)
    print(email)
