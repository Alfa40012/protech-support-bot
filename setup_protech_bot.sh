from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

BOT_TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"
WHATSAPP_LINK = "https://wa.me/message/2JZ4HHC5JOSFC1"
CHANNEL_LINK = "https://t.me/ProTechSupport1Bot"
FILE_CHANNEL = "https://www.mediafire.com/file/vm2khd0dnemy7ro/"

WELCOME_MSG = """
👋 مرحبًا بك في بوت الدعم الفني لـ PROTECH IPTV

🤖 البوت يعمل تلقائيًا وعلى مدار الساعة.
📡 إذا واجهت أي مشكلة أو تحتاج للمساعدة، اختر من القائمة بالأسفل أو أرسل كود MAC الخاص بجهازك.

📍 تأكد من:
- فصل الراوتر من الكهرباء لمدة دقيقة
- إعادة تشغيل الجهاز
"""

AUTO_REPLY = """
✅ السيرفر يعمل بكفاءة ✅

يرجى التأكد من:
1. فصل الروتر من الكهرباء لمدة دقيقة
2. إعادة تشغيل الجهاز
3. الانتظار قليلاً حتى يعمل السيرفر

📞 إذا استمرت المشكلة ➜ تواصل معنا عبر واتساب 👇
"""

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📡 فحص الكود / الدعم الفني", callback_data="support")],
        [InlineKeyboardButton("📥 تحميل ملف القنوات", callback_data="channels")],
        [InlineKeyboardButton("💳 تجديد الاشتراك", callback_data="renew")],
        [InlineKeyboardButton("🛒 شراء الأجهزة أونلاين", url="https://rafal.giize.com/")],
        [InlineKeyboardButton("💬 تواصل مع الدعم على واتساب", url=WHATSAPP_LINK)],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo="https://i.top4top.io/p_3485uoxkw0.jpg",
        caption=WELCOME_MSG,
        reply_markup=get_main_menu()
    )

async def handle_mac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if any(x in text for x in ["MAC", ":", "-"]) or len(text) >= 10:
        await update.message.reply_text(AUTO_REPLY)
        await update.message.reply_text("💬 يمكنك التواصل مباشرة مع الدعم عبر واتساب:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 اضغط هنا", url=WHATSAPP_LINK)]
        ]))
    else:
        await update.message.reply_text("🛠 من فضلك أرسل كود MAC أو اختر الخدمة من القائمة:", reply_markup=get_main_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "support":
        await query.edit_message_text(
            "🛠 من فضلك أرسل نوع الجهاز وكود MAC الخاص بك وسيتم الرد عليك مباشرة.\n\nمثال:\n✅ نوع الجهاز: REDLINE\n✅ MAC: 162CBD932D7A"
        )
    elif query.data == "channels":
        await query.edit_message_text(
            f"📥 لتحميل أحدث ملف قنوات نايل سات:\n[اضغط هنا]({FILE_CHANNEL})",
            parse_mode="Markdown"
        )
    elif query.data == "renew":
        await query.edit_message_text(
            "💳 لتجديد الاشتراك:\n1. أرسل كود MAC الخاص بك\n2. سيتم مراجعة الاشتراك وإبلاغك بالتجديد\n\nأو تواصل على واتساب:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 واتساب للتجديد", url=WHATSAPP_LINK)]
            ])
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mac))
    app.run_polling()
