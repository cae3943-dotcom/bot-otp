import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# DAFTAR AKUN EMAIL SENDER (AUTO-ROTATE)
# ==========================================
# Lu bisa nambah 2, 3, atau banyak email sekaligus nanti di sini!
EMAIL_ACCOUNTS = [
    {
        "email": "rahmatid27@gmail.com",    # Ganti email 1
        "password": "avgj qaef ggru yuuy"          # Paste kode 16 digit tadi
    },
    # Kalau ada email ke-2, buka pagar (#) di bawah ini:
    # {
    #     "email": "rahmatjametgg@gmail.com",
    #     "password": "tsxi rvcv agbu lyjj"
    # }
]

current_email_index = 0

def get_next_email():
    """Mengambil email pengirim bergantian (Round-Robin)."""
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
    
    # Rapiin nomor jadi list kebawah
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
        # Ganti ke SSL Port 465 (Lebih stabil di server cloud/Railway)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, target_email, msg.as_string())
        server.quit()
        return True, smtp_email
    except Exception as e:
        return False, str(e)
