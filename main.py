from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

WELCOME_TEXT = "👋 أهلاً بك في خدمة الدعم الفني لشركة PROTECH IPTV.\nيرجى اختيار الخدمة المطلوبة من القائمة التالية 👇"

# روابط الملفات
SOFTWARE_LINK = "https://www.mediafire.com/file/vm2khd0dnemy7ro/latest-protech-nilesat.bin/file"
CHANNELS_FILE_LINK = "https://www.mediafire.com/file/vm2khd0dnemy7ro/latest-channels-protech.bin/file"
WHATSAPP_LINK = "https://wa.me/message/2JZ4HHC5JOSFC1"

# المنيو منظمة بشكل أفقي وجميل
MAIN_MENU = [
    [
        InlineKeyboardButton("📥 سوفت PROTECH PW10", callback_data="download_soft"),
        InlineKeyboardButton("📡 ملف قنوات", callback_data="channels")
    ],
    [
        InlineKeyboardButton("📺 تفعيل IPTV", callback_data="iptv_activate"),
        InlineKeyboardButton("🧪 فحص كود MAC", callback_data="check_mac")
    ],
    [
        InlineKeyboardButton("❓ مشاكل IPTV أو النت", callback_data="diagnose")
    ],
    [
        InlineKeyboardButton("📞 تواصل مع الدعم عبر واتساب", url=WHATSAPP_LINK)
    ]
]

# الردود حسب اختيار المستخدم
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(MAIN_MENU)
    if update.message:
        await update.message.reply_text(WELCOME_TEXT, reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.edit_message_text(WELCOME_TEXT, reply_markup=keyboard)

# لما يضغط المستخدم على زر
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "download_soft":
        await query.edit_message_text(f"⬇️ لتحميل السوفت:\n{SOFTWARE_LINK}")
    elif query.data == "channels":
        await query.edit_message_text(f"📺 لتحميل ملف القنوات:\n{CHANNELS_FILE_LINK}")
    elif query.data == "check_mac":
        await query.edit_message_text("🔍 من فضلك أرسل كود MAC الخاص بجهازك.")
    elif query.data == "diagnose":
        await query.edit_message_text("🧪 من فضلك صف مشكلتك وسنقوم بمساعدتك.")
    elif query.data == "iptv_activate":
        await query.edit_message_text("📺 لتفعيل IPTV، من فضلك أرسل:\n1- نوع الجهاز\n2- اسم السيرفر المراد التفعيل عليه")
    else:
        await send_main_menu(update, context)

# لو أرسل المستخدم رسالة نصية (مثل كود MAC أو شرح مشكلة)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # فحص كود MAC
    if ":" in text or len(text) == 12:
        await update.message.reply_text("✅ تم استلام كود MAC، سيتم فحصه وربط الجهاز بالخدمة.")
    elif any(x in text.lower() for x in ["iptv", "server", "protech", "pw10", "nova"]):
        await update.message.reply_text("📌 تم استلام معلومات التفعيل، سيتم التحقق والتفعيل خلال دقائق.")
    else:
        await update.message.reply_text("📨 شكراً لتواصلك، سيتم الرد عليك من الدعم الفني قريباً.")

# البرنامج الأساسي
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", send_main_menu))  # start
    app.add_handler(CallbackQueryHandler(handle_buttons))      # منيو الأزرار
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # الرسائل النصية

    print("✅ البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
