import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

def send_wa_appeal(number_list):
    """Mengirimkan email unban batch ke WhatsApp Support via Resend API."""
    formatted_numbers = "\n".join([f"- +{str(num).strip().replace('+', '')}" for num in number_list])
    
    email_body = f"""Hello WhatsApp Support Team,

I am having trouble receiving the SMS verification code and logging into my account. It says "Login unavailable for now" and "Couldn't send an SMS".

I am using the official WhatsApp app and my phone number is active. Please help me fix this system restriction so I can log in.

My phone numbers:
{formatted_numbers}

Thank you for your help."""

    params = {
        "from": "WhatsApp Support <onboarding@resend.dev>",
        "to": ["support@support.whatsapp.com"],
        "subject": "Request assistance for WhatsApp account access",
        "text": email_body,
    }

    try:
        response = resend.Emails.send(params)
        if response and "id" in response:
            return True, "Resend API"
        else:
            return False, f"Resend Error: {str(response)}"
    except Exception as e:
        return False, str(e)
        
