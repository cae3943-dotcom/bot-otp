import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import fix_merah

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token Bot Telegram Khusus Fix Merah (Ambil dari BotFather)
BOT_TOKEN = os.getenv("FIX_MERAH_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🤖 <b>Bot Fix Merah WhatsApp Ready!</b>\n\n"
        "Kirimkan atau paste daftar nomor WhatsApp yang terblokir (merah).\n"
        "<i>Maksimal 10 nomor per sekali kirim/batch.</i>\n\n"
        "Contoh format:\n"
        "628123456789\n"
        "628987654321"
    )
    await update.message.reply_text(welcome_text, parse_mode="HTML")

async def handle_fix_merah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Ekstrak semua pola nomor telepon (10 sampai 15 digit angka)
    raw_numbers = re.findall(r'\+?\d{10,15}', text)
    
    if not raw_numbers:
        await update.message.reply_text("❌ Tidak ada nomor valid yang ditemukan. Pastikan format nomor benar.")
        return
        
    # Batasi maksimal 10 nomor per batch agar aman
    numbers = list(set(raw_numbers))[:10]
    
    status_msg = await update.message.reply_text(f"⏳ Sedang mengirimkan email appeal untuk {len(numbers)} nomor ke WhatsApp Support...", parse_mode="HTML")
    
    # Eksekusi kirim email via fix_merah.py
    success, result = fix_merah.send_wa_appeal(numbers)
    
    if success:
        nums_text = "\n".join([f"• +{n.strip().replace('+', '')}" for n in numbers])
        reply = (
            f"✅ <b>Sukses Pengajuan Fix Merah!</b>\n\n"
            f"📧 <b>Sender:</b> <code>{result}</code>\n"
            f"📱 <b>Nomor Diproses ({len(numbers)}/10):</b>\n{nums_text}\n\n"
            f"<i>Appeal telah dikirim ke support@support.whatsapp.com</i>"
        )
    else:
        reply = f"❌ <b>Gagal mengirim email:</b> {result}"
        
    await status_msg.edit_text(reply, parse_mode="HTML")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_fix_merah))
    
    print("Bot Fix Merah sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
      
