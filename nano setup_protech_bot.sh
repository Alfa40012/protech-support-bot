import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# إعدادات البوت
BOT_TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"
CHANNELS_FILE = "assets/latest_channels.txt"
WHATSAPP_URL = "https://wa.me/message/2JZ4HHC5JOSFC1"

logging.basicConfig(level=logging.INFO)

# ✅ رسالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🇸🇦 عربي", callback_data="lang_ar")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ]
    await update.message.reply_text("Welcome to PROTECH Support Bot\nيرجى اختيار اللغة / Please choose language:", reply_markup=InlineKeyboardMarkup(buttons))

# ✅ اختيار اللغة
async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data
    context.user_data["lang"] = lang

    if lang == "lang_ar":
        text = "مرحبًا بك في بوت دعم PROTECH.\nاختر من القائمة:"
        buttons = [
            [InlineKeyboardButton("📡 ملف القنوات", callback_data="channels")],
            [InlineKeyboardButton("📥 تحميل السوفت", callback_data="software")],
            [InlineKeyboardButton("🔁 تجديد الاشتراك", callback_data="renew")],
            [InlineKeyboardButton("🛠️ تشخيص مشاكل IPTV/النت", callback_data="diagnose")],
            [InlineKeyboardButton("📞 دعم واتساب", url=WHATSAPP_URL)]
        ]
    else:
        text = "Welcome to PROTECH Support Bot.\nPlease choose from the menu:"
        buttons = [
            [InlineKeyboardButton("📡 Channels File", callback_data="channels")],
            [InlineKeyboardButton("📥 Software Download", callback_data="software")],
            [InlineKeyboardButton("🔁 Renew Subscription", callback_data="renew")],
            [InlineKeyboardButton("🛠️ Diagnose IPTV/Internet", callback_data="diagnose")],
            [InlineKeyboardButton("📞 WhatsApp Support", url=WHATSAPP_URL)]
        ]

    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

# ✅ الرد على الأوامر
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data
    lang = context.user_data.get("lang", "lang_ar")

    if choice == "channels":
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        await query.message.reply_text(f"📡 أحدث ملف قنوات نايل سات:\n\n{content}")

    elif choice == "software":
        await query.message.reply_text("📥 يرجى إرسال موديل الجهاز مثل: PROTECH PW10")

    elif choice == "renew":
        msg = "للتجديد، أرسل لنا صورة الاشتراك القديم أو MAC." if lang == "lang_ar" else "To renew, send us your old subscription or MAC."
        await query.message.reply_text(msg)

    elif choice == "diagnose":
        msg = "🚀 لفحص مشاكل الإنترنت أو IPTV، أرسل صورة من القناة أو رقم MAC أو وصف المشكلة." if lang == "lang_ar" else "🚀 To diagnose issues, send channel image, MAC or problem details."
        await query.message.reply_text(msg)

# ✅ الرد على MAC أو موديل الجهاز
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if "PROTECH PW10" in text:
        await update.message.reply_text("✅ لتحميل السوفت الخاص بجهاز PROTECH PW10:\n👇 اضغط هنا:\nhttps://www.mediafire.com/file/xxxxxxx")

    elif len(text) == 12 and ":" not in text:
        await update.message.reply_text(f"🔍 تم استلام MAC: {text}\nسيتم فحصه وإبلاغك بالنتيجة قريبًا.")

    else:
        await update.message.reply_text("✅ تم استلام رسالتك، وسيتم الرد عليك من الدعم قريبًا.")

# ✅ تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(choose_language, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(handle_menu, pattern="^(channels|software|renew|diagnose)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ BOT is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
