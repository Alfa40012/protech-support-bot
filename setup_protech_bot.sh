import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler, ContextTypes
)

# إعدادات البوت
BOT_TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"
CHANNEL_FILE_URL = "https://www.mediafire.com/file/vm2khd0dnemy7ro/PROTECH_Nilesat_Channel_List.rar"
WHATSAPP_RENEW_URL = "https://wa.me/p/10036792293099711/201098256570"
WHATSAPP_SHOP_URL = "https://wa.me/c/201098256570"

logging.basicConfig(level=logging.INFO)

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
    ]
    await update.message.reply_text("👋 اختر لغتك / Choose your language:", reply_markup=InlineKeyboardMarkup(keyboard))

# اختيار اللغة
async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang

    if lang == "ar":
        await query.edit_message_text(
            "🎉 مرحبًا بك في دعم PROTECH IPTV\nاختر خدمة من القائمة:",
            reply_markup=main_menu_ar()
        )
    else:
        await query.edit_message_text(
            "🎉 Welcome to PROTECH IPTV Support\nChoose a service:",
            reply_markup=main_menu_en()
        )

# منيو رئيسي (عربي)
def main_menu_ar():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📡 تحميل ملف القنوات", callback_data="channels")],
        [InlineKeyboardButton("🔁 تجديد الاشتراك", url=WHATSAPP_RENEW_URL)],
        [InlineKeyboardButton("🛒 شراء أونلاين", url=WHATSAPP_SHOP_URL)],
        [InlineKeyboardButton("🧑‍💻 الدعم الفني", url="https://wa.me/message/2JZ4HHC5JOSFC1")]
    ])

# منيو رئيسي (إنجليزي)
def main_menu_en():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📡 Download Channel File", callback_data="channels")],
        [InlineKeyboardButton("🔁 Renew Subscription", url=WHATSAPP_RENEW_URL)],
        [InlineKeyboardButton("🛒 Buy Online", url=WHATSAPP_SHOP_URL)],
        [InlineKeyboardButton("🧑‍💻 Technical Support", url="https://wa.me/message/2JZ4HHC5JOSFC1")]
    ])

# الرد على اختيار "ملف القنوات"
async def handle_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "channels":
        lang = context.user_data.get("lang", "ar")
        msg = "📡 إليك ملف القنوات:\n" if lang == "ar" else "📡 Here is the channel file:\n"
        await query.edit_message_text(f"{msg}[اضغط هنا للتحميل]({CHANNEL_FILE_URL})", parse_mode="Markdown")

# الرد على رسائل MAC Address
async def handle_mac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if len(text) == 12 and all(c in "0123456789ABCDEF" for c in text):
        await update.message.reply_text(f"✅ تم استلام كود MAC:\n{text}\n🔄 سيتم فحص الاشتراك والتواصل معك قريبًا.")
    else:
        await update.message.reply_text("❌ الكود غير صحيح. الرجاء إرسال MAC مكوّن من 12 رقم/حرف (Hex).")

# رد عام على أي رسالة أخرى
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 أرسل MAC الخاص بجهازك أو استخدم الأزرار في القائمة.")

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_selected, pattern="lang_.*"))
    app.add_handler(CallbackQueryHandler(handle_menu_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mac))
    app.add_handler(MessageHandler(filters.ALL, unknown))

    print("🤖 Bot is running...")
    app.run_polling()
