from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

menu = [
    ["📡 تشخيص الجهاز", "🎥 تحميل السوفت"],
    ["💡 حلول سريعة", "📲 تفعيل IPTV"],
    ["📞 تواصل مع الدعم", "📍 فنيين معتمدين"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text("👋 أهلاً بك في دعم PROTECH الرسمي\n\nاختر الخدمة التي تحتاجها:", reply_markup=keyboard)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if "تشخيص" in msg:
        await update.message.reply_text("📡 أرسل كود الجهاز (MAC أو SN).")
    elif "السوفت" in msg:
        await update.message.reply_text("🎥 جاري تجهيز روابط السوفت...")
    elif "حلول" in msg:
        await update.message.reply_text("💡 أكثر المشاكل:\n- التهنيج\n- IPTV لا يعمل\nجرب إعادة التشغيل.")
    elif "IPTV" in msg:
        await update.message.reply_text("📲 أرسل كود التفعيل.")
    elif "الدعم" in msg:
        await update.message.reply_text("📞 تواصل: @ProTechSupportTeam")
    elif "فنيين" in msg:
        await update.message.reply_text("📍 أرسل موقعك لنرشح أقرب فني.")
    else:
        await update.message.reply_text("❓ لم أفهم، اختر من القائمة.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ البوت يعمل الآن...")
app.run_polling()
