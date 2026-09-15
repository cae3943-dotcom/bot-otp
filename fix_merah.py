import requests

EMAILJS_SERVICE_ID = "service_2m9cwno"
EMAILJS_TEMPLATE_ID = "template_8tl0w5g"
EMAILJS_PUBLIC_KEY = "GELSNvIZ5Z7NrKSLJ"

def send_wa_appeal(number_list):
    """Mengirimkan email unban batch ke WhatsApp Support via EmailJS HTTP API."""
    url = "https://api.emailjs.com/api/v1.0/email/send"
    
    # Format nomor handphone jadi rapi berbaris
    formatted_numbers = "\n".join([f"- +{str(num).strip().replace('+', '')}" for num in number_list])
    
    payload = {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_PUBLIC_KEY,
        "template_params": {
            "message": formatted_numbers
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            return True, "EmailJS (HTTP API)"
        else:
            return False, f"EmailJS Error ({response.status_code}): {response.text}"
    except Exception as e:
        return False, str(e)
        
