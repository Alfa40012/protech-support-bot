from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

# بيانات البوت
BOT_TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

# رسالة الترحيب
WELCOME_TEXT = """
🎉 أهلاً بك في بوت الدعم الفني لشركة PROTECH IPTV!

اختر الخدمة التي تحتاجها من القائمة أدناه، أو أرسل لنا استفسارك مباشرة.

🛡 البوت يعمل 24/7 لخدمتك.
"""

# منيو البداية
def start_menu():
    keyboard = [
        [
            InlineKeyboardButton("📥 تحميل السوفت", callback_data="soft"),
            InlineKeyboardButton("📡 ملف قنوات نايل سات", callback_data="channels"),
        ],
        [
            InlineKeyboardButton("💳 تفعيل IPTV", callback_data="iptv"),
        ],
        [
            InlineKeyboardButton("📶 مشاكل الإنترنت", callback_data="net"),
        ],
        [
            InlineKeyboardButton("🛠 دعم فني مباشر", callback_data="support"),
            InlineKeyboardButton("📞 تواصل واتساب", url="https://wa.me/message/2JZ4HHC5JOSFC1"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=start_menu())

# الرد على الأزرار
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "soft":
        await query.edit_message_text("📥 لتحميل السوفت، اضغط هنا:\n[تحميل السوفت](https://www.mediafire.com/file/vm2khd0dnemy7ro/soft.bin)", parse_mode="Markdown")
    elif data == "channels":
        await query.edit_message_text("📡 لتحميل ملف القنوات (نايل سات عربي)، اضغط هنا:\n[ملف القنوات](https://www.mediafire.com/file/vm2khd0dnemy7ro/soft.bin)", parse_mode="Markdown")
    elif data == "iptv":
        await query.edit_message_text("💳 من فضلك أرسل:\n- نوع الجهاز\n- MAC Address (ماك الجهاز)\n- اسم السيرفر المطلوب تفعيله")
    elif data == "support":
        await query.edit_message_text("🛠 يرجى إرسال مشكلتك بالتفصيل وسيتم الرد عليك من فريق الدعم.\n\n🔄 أو تواصل مباشرة عبر واتساب:\nhttps://wa.me/message/2JZ4HHC5JOSFC1")
    elif data == "net":
        await query.edit_message_text("📶 لحل مشاكل الإنترنت:\n\n1. افصل فيشة الراوتر وشغله تاني.\n2. جرب تعمل هوت سبوت من الموبايل للرسيفر.\n3. لو المشكلة مستمرة، جرب من شبكة تانية.\n4. أو توجّه لأقرب مركز صيانة.")

# الرد على إرسال MAC أو أي استفسار
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ":" in text and len(text) >= 12:
        await update.message.reply_text("✅ تم استلام MAC: " + text + "\nجاري التحقق من البيانات وسيتم التواصل معك قريبًا.")
    else:
        await update.message.reply_text("📬 شكرًا لتواصلك معنا، سيتم الرد عليك قريبًا من الدعم الفني.")

# تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ BOT IS RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
