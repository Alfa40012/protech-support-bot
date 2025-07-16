from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

# القوائم حسب اللغة
menu_ar = [
    ["📡 تشخيص MAC", "🎥 تحميل السوفت"],
    ["📺 ملف قنوات", "🔁 تجديد الاشتراك"],
    ["💬 تواصل واتساب"]
]

# المستخدمين ولغتهم
user_lang = {}

# رسالة ترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_lang[user_id] = None  # إعادة اللغة لاختيار جديد

    # أرسل صورة اللوجو
    await update.message.reply_photo(
        photo="https://i.imgur.com/k8D0Omv.png",  # رابط صورة اللوجو
        caption="🔰 PROTECH SUPPORT\n\n👋 مرحبًا بك في البوت الرسمي للدعم الفني\n\nيرجى اختيار اللغة:",
        reply_markup=ReplyKeyboardMarkup([["🇸🇦 العربية", "🇬🇧 English"]], resize_keyboard=True)
    )

# التعامل مع الرسائل
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    msg = update.message.text

    # تحديد اللغة
    if msg == "🇸🇦 العربية":
        user_lang[user_id] = "ar"
        keyboard = ReplyKeyboardMarkup(menu_ar, resize_keyboard=True)
        await update.message.reply_text("✅ تم اختيار اللغة العربية.\nاختر من القائمة:", reply_markup=keyboard)
        return

    elif msg == "🇬🇧 English":
        await update.message.reply_text("❌ English support coming soon.")
        return

    # الردود العربية
    if user_lang.get(user_id) == "ar":
        if "MAC" in msg or ":" in msg:
            await update.message.reply_text("📡 من فضلك أرسل رقم MAC مثل:\n`00:1A:79:12:34:56`")
        elif "السوفت" in msg:
            await update.message.reply_text("🎥 من فضلك اختر موديل الجهاز:\n- Protech Mini\n- Protech X5\n- Protech Ultra Max")
        elif "قنوات" in msg:
            await update.message.reply_text(
                "📺 أحدث ملف قنوات - نايل سات عربي\n\n"
                "⬇️ لتحميل الملف:\n"
                "[اضغط هنا](https://www.mediafire.com/file/vm2khd0dnemy7ro/...)",
                parse_mode="Markdown"
            )
        elif "الاشتراك" in msg:
            await update.message.reply_text("🔁 أرسل رقم الاشتراك أو الكود لتجديد الخدمة.")
        elif "واتساب" in msg:
            whatsapp_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("📞 اضغط للتواصل", url="https://wa.me/message/2JZ4HHC5JOSFC1")]
            ])
            await update.message.reply_text("💬 تواصل مباشر عبر واتساب:", reply_markup=whatsapp_button)
        else:
            await update.message.reply_text("❓ لم أفهم، اختر من القائمة.")

    else:
        await update.message.reply_text("👋 من فضلك اختر اللغة أولاً:", reply_markup=ReplyKeyboardMarkup([["🇸🇦 العربية", "🇬🇧 English"]], resize_keyboard=True))

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ البوت شغال الآن...")
app.run_polling()
