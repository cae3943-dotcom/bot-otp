import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ==========================================
# DAFTAR AKUN EMAIL SENDER (AUTO-ROTATE)
# ==========================================
EMAIL_ACCOUNTS = [
    {
        "email": "rahmatid27@gmail.com",       # Ganti email Gmail lu
        "password": "avgj qaef ggru yuuy"       # App Password 16 digit
    },
    
    {
        "email": "rahmatjametgg@gmail.com",
        "password": "tsxi rvcv agbu lyjj"
    },
]

current_email_index = 0

def get_next_email():
    """Mengambil email pengirim secara bergantian (Round-Robin)."""
    global current_email_index
    account = EMAIL_ACCOUNTS[current_email_index]
    current_email_index = (current_email_index + 1) % len(EMAIL_ACCOUNTS)
    return account

def send_wa_appeal(number_list):
    """Mengirimkan email unban batch (max 10 nomor) ke WhatsApp Support."""
    target_email = "support@support.whatsapp.com"
    
    sender_acc = get_next_email()
    smtp_email = sender_acc["email"]
    smtp_password = sender_acc["password"]
    
    formatted_numbers = "\n".join([f"- +{str(num).strip().replace('+', '')}" for num in number_list])
    
    subject = "My account was deactivated by mistake"
    body = f"""Hello WhatsApp Support Team,

My phone numbers were deactivated without any prior warning. I believe this was done by mistake as I always follow the Terms of Service.

Please review and unblock my phone numbers below:
{formatted_numbers}

I need these numbers urgently for my daily communication. Thank you for your assistance.
"""

    msg = MIMEMultipart()
    msg['From'] = smtp_email
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Force koneksi pakai IPv4 biar gak kena Errno 101 Network is unreachable di Railway
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_socket.settimeout(15)
        raw_socket.connect(("smtp.gmail.com", 587))
        
        server = smtplib.SMTP(host="smtp.gmail.com", port=587, timeout=15)
        server.sock = raw_socket
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, target_email, msg.as_string())
        server.quit()
        return True, smtp_email
    except Exception as e:
        return False, str(e)
