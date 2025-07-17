# Bot by ProTech IPTV - Telegram: @ProTechSupport1Bot

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

# روابط ثابتة
WHATSAPP_LINK = "https://wa.me/message/2JZ4HHC5JOSFC1"
SOFT_URL = "https://www.mediafire.com/file/07cudmx5w3x65tb/SOFT_PROTECH.rar/file"
CHANNEL_URL = "https://t.me/ProtechIPTV"
FILE_CHANNEL_URL = "https://www.mediafire.com/file/vm2khd0dnemy7ro/Nile_Sat_Arabic_TP_PROTECH.abs/file"

# رسائل جاهزة
WELCOME_MSG = """👋 مرحبًا بك في بوت دعم PROTECH  الرسمي!

🤖 البوت يعمل تلقائيًا 24 ساعة.

📍 استخدم الأزرار التالية للحصول على الخدمات:
"""

HELP_MSG = """🆘 *طريقة استخدام البوت:*

• اختر من القائمة الخدمة التي تحتاجها.
• أو أرسل كود MAC أو اسم جهازك مباشرة.
• للتواصل مع الدعم، اضغط على زر واتساب.

📌 البوت يعمل 24/7 لخدمتك.

*PROTECH IPTV — نخدمك بكل احترافية*
"""

CHANNEL_MSG = f"""📡 *ملف القنوات - نايل سات عربي* 

🔹 يحتوي على جميع القنوات المحدثة بجودة عالية.

📥 لتحميل الملف اضغط على الزر أدناه.
"""

SOFT_MSG = """🛠️ *تحديث السوفت وير الرسمي لأجهزة PROTECH* 

📦 يشمل:
- دعم كامل لأحدث القنوات
- تحسين الأداء وحل مشاكل التهنيج
- تحديثات تلقائية مستقبلًا

📥 اضغط الزر أدناه لتحميل السوفت."""
 
# منيو رئيسية
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ فحص الكود / الدعم الفني", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("📡 ملف القنوات", callback_data="channels")],
        [InlineKeyboardButton("🛠️ سوفت الجهاز", callback_data="soft")],
        [InlineKeyboardButton("ℹ️ مساعدة", callback_data="help")],
    ])

# دالة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MSG, reply_markup=main_menu())

# دالة المساعدة
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MSG, parse_mode="Markdown")

# استقبال أي MAC أو اسم جهاز
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if len(text) >= 10:
        await update.message.reply_text(f"""📩 تم استلام الكود / اسم الجهاز:

`{text}`

🧑‍💻 سيتم مراجعته من الدعم الفني.

للتواصل المباشر:
👉 [اضغط هنا]({WHATSAPP_LINK})""", parse_mode="Markdown")
    else:
        await update.message.reply_text("📌 برجاء إرسال كود الجهاز أو اسم الجهاز بشكل صحيح.")

# معالجة الضغط على الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "channels":
        await query.message.reply_text(CHANNEL_MSG, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 تحميل الملف", url=FILE_CHANNEL_URL)]
        ]), parse_mode="Markdown")
    elif data == "soft":
        await query.message.reply_text(SOFT_MSG, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 تحميل السوفت", url=SOFT_URL)]
        ]), parse_mode="Markdown")
    elif data == "help":
        await query.message.reply_text(HELP_MSG, parse_mode="Markdown")

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 ProTechSupport1Bot is running 24/7...")
    app.run_polling()
