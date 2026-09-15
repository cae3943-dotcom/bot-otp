import os
import requests

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")

def send_wa_appeal(number_list):
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    formatted_numbers = "\n".join([f"- +{str(num).strip().replace('+', '')}" for num in number_list])

    email_body = f"""Hello WhatsApp Support Team,

I am having trouble receiving the SMS verification code and logging into my account. It says "Login unavailable for now" and "Couldn't send an SMS".

I am using the official WhatsApp app and my phone number is active. Please help me fix this system restriction so I can log in.

My phone numbers:
{formatted_numbers}

Thank you for your help."""

    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": f"WhatsApp Support <mailgun@{MAILGUN_DOMAIN}>",
        "to": ["support@support.whatsapp.com"],
        "subject": "Request assistance for WhatsApp account access",
        "text": email_body
    }

    try:
        response = requests.post(url, auth=auth, data=data, timeout=15)
        if response.status_code == 200:
            return True, "Mailgun API"
        else:
            return False, f"Mailgun Error ({response.status_code}): {response.text}"
    except Exception as e:
        return False, str(e)
        
