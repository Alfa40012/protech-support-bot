from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)

# بيانات البوت
TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"
ADMIN_ID = 907876903
WELCOME_IMAGE = "https://g.top4top.io/p_3486pis4c0.jpg"
WHATSAPP_LINK = "https://wa.me/message/2JZ4HHC5JOSFC1"

# قائمة الاختيارات الرئيسية
main_menu = [
    [KeyboardButton("🔧 مشاكل السوفت")],
    [KeyboardButton("📺 موديل الرسيفر")],
    [KeyboardButton("🌐 روابط القنوات")]
]
menu_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# دالة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=WELCOME_IMAGE,
        caption="مرحبًا بك في خدمة الدعم الفني 📡\nاختر من القائمة التالية 👇",
        reply_markup=menu_markup
    )

# دالة التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    # إرسال تنبيه للإدمن بكل رسالة
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 رسالة جديدة من: {user_name} (ID: {user_id})\n\n💬 {user_message}"
    )

    # ردود على الاختيارات
    if user_message == "🔧 مشاكل السوفت":
        await update.message.reply_text("🛠️ من فضلك صف نوع مشكلة السوفت التي تواجهها بالتفصيل...")
    elif user_message == "📺 موديل الرسيفر":
        await update.message.reply_text("📝 من فضلك اكتب موديل الرسيفر الخاص بك وسنساعدك...")
    elif user_message == "🌐 روابط القنوات":
        await update.message.reply_text("📡 إليك بعض روابط القنوات:\n\n✅ [قناة 1](http://example.com/1)\n✅ [قناة 2](http://example.com/2)", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ لم يتم التعرف على الأمر.\n💬 تواصل مع الدعم عبر واتساب:\n{WHATSAPP_LINK}")

# تشغيل التطبيق
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
