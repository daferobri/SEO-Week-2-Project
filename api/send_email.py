import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

# params: resend.Emails.SendParams = {
#   "from": "Acme <onboarding@resend.dev>",
#   "to": ["daferobri5941@gmail.com"],
#   "subject": "hello world",
#   "html": "<p>it works!</p>"
# }

# email = resend.Emails.send(params)
# print(email)