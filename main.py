from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re

# ✅ توكن البوت
TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

# ✅ صورة اللوجو (ارفعها عندك أو استخدم ملف محلي مؤقتًا)
LOGO_PATH = "protech_logo.jpg"  # حط هنا اسم ملف اللوجو الموجود بجوار السكربت

# ✅ روابط مهمة
WHATSAPP_URL = "https://wa.me/message/2JZ4HHC5JOSFC1"
CHANNELS_URL = "https://www.mediafire.com/file/vm2khd0dnemy7ro/%25D8%25B5%25D9%2586_%25D8%25A8%25D9%2584%25D8%25B5_%25D8%25AF%25D8%25A7%25D9%2583%25D9%2589_%25D9%2586%25D8%25A7%25D9%258A%25D9%2584_%25D8%25B9%25D8%25B1%25D8%25A8%25D9%2589.bin/file"
WEBSITE_URL = "https://www.rafal.giize.com/"

# ✅ المنيو التفاعلي بالعربي
menu = [
    ["📡 تشخيص الجهاز", "🎥 تحميل السوفت"],
    ["💡 حلول سريعة", "📲 تفعيل IPTV"],
    ["📞 تواصل مع الدعم", "📍 فنيين معتمدين"],
    ["📺 ملف القنوات", "💬 تواصل واتساب"]
]

# ✅ أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    chat_id = update.effective_chat.id

    # إرسال اللوجو أولاً
    try:
        with open(LOGO_PATH, "rb") as logo:
            await context.bot.send_photo(chat_id=chat_id, photo=logo)
    except Exception as e:
        print("❌ لم يتم العثور على اللوجو:", e)

    await update.message.reply_text(
        "👋 أهلاً بك في دعم PROTECH الرسمي\n\nاختر الخدمة التي تحتاجها:",
        reply_markup=keyboard
    )

# ✅ التعامل مع الرسائل
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    chat_id = update.effective_chat.id

    # أوامر بداية
    if msg.lower() in ["start", "/start", "ابدأ"]:
        await start(update, context)
        return

    # تحقق من MAC تلقائيًا
    if re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", msg):
        await update.message.reply_text("✅ تم استلام MAC، جارٍ التحقق...")
        return

    # الأوامر
    if "تشخيص" in msg:
        await update.message.reply_text("📡 أرسل MAC أو SN للجهاز الآن.")
    elif "السوفت" in msg:
        await update.message.reply_text("🎥 سيتم توفير روابط السوفت المناسب حسب الموديل قريبًا.")
    elif "حلول" in msg:
        await update.message.reply_text("💡 أكثر المشاكل:\n- تهنيج\n- IPTV لا يعمل\n🔁 جرب إعادة التشغيل.")
    elif "IPTV" in msg:
        await update.message.reply_text("📲 أرسل كود التفعيل الخاص بك.")
    elif "الدعم" in msg:
        await update.message.reply_text("📞 للتواصل: @ProTechSupportTeam")
    elif "فنيين" in msg:
        await update.message.reply_text("📍 أرسل موقعك وسنخبرك بأقرب فني معتمد.")
    elif "القنوات" in msg:
        await update.message.reply_text(f"📺 ملف قنوات نايل سات (عربي):\n[اضغط هنا لتحميله]({CHANNELS_URL})", parse_mode="Markdown")
    elif "واتساب" in msg:
        await update.message.reply_text(f"💬 تواصل مع خدمة العملاء عبر واتساب:\n[اضغط هنا]({WHATSAPP_URL})", parse_mode="Markdown")
    else:
        await update.message.reply_text("❓ لم أفهم طلبك، الرجاء اختيار خيار من القائمة.")

# ✅ إعداد التطبيق
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ البوت يعمل الآن...")
app.run_polling()
