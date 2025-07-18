import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# بيانات البوت
BOT_TOKEN = '7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I'
bot = telebot.TeleBot(BOT_TOKEN)

# روابط ملفات القنوات
CHANNELS_MESSAGE = """
⁦⚠️⁩ *حصرياً قبل أي حد* ⁦⚠️⁩
*🧩 أحدث ملف قنوات صن بلص:*
- 2507L - 1507DK - 1506tv - hv
- نايل سات عربي ✅ متحرك عربي ✅
- بتاريخ: 2025/7/1

✅ تم إضافة:
• قناة بين الإخبارية
• قناة دوللي كلاسيك
• قناة العاصمة الجديدة

📡 *نايل سات عربي:* 
[اضغط هنا للتحميل](https://www.mediafire.com/file/ww5cz83z2ot5p2j/صن+بلص+داكى+نايل+سات+عربي+شهر+7.bin/file)

📡 *متحرك عربي:* 
[اضغط هنا للتحميل](https://www.mediafire.com/file/q19ps221mcu2u73/)
"""

# روابط السوفتات حسب الموديل (مثال)
SOFTWARE_LINKS = {
    "1506tv": "https://www.mediafire.com/folder/XXXXXX/1506tv",
    "2507L": "https://www.mediafire.com/folder/YYYYYY/2507L",
    "1507DK": "https://www.mediafire.com/folder/ZZZZZZ/1507DK",
}

# رسالة ترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🇪🇬 العربية", callback_data="lang_ar"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    bot.send_message(message.chat.id, "👋 مرحباً بك في *PROTECH IPTV Support Bot*\nيرجى اختيار اللغة:", reply_markup=markup, parse_mode="Markdown")

# اللغة العربية: منيو الخدمات
def main_menu_ar(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📥 تحميل السوفت", callback_data="soft_ar"),
        InlineKeyboardButton("📺 ملفات القنوات", callback_data="channels_ar"),
    )
    markup.add(
        InlineKeyboardButton("♻️ تجديد الاشتراك", url="https://wa.me/p/10036792293099711/201098256570"),
        InlineKeyboardButton("🛒 شراء أون لاين", url="https://wa.me/c/201098256570"),
    )
    markup.add(
        InlineKeyboardButton("🧠 تشخيص مشاكل الجهاز", callback_data="diagnose_ar")
    )
    bot.send_message(chat_id, "👇 اختر الخدمة المطلوبة:", reply_markup=markup)

# اختيار اللغة
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "lang_ar":
        main_menu_ar(call.message.chat.id)

    elif call.data == "channels_ar":
        bot.send_message(call.message.chat.id, CHANNELS_MESSAGE, parse_mode="Markdown")

    elif call.data == "soft_ar":
        markup = InlineKeyboardMarkup()
        for model in SOFTWARE_LINKS:
            markup.add(InlineKeyboardButton(f"🔽 {model}", url=SOFTWARE_LINKS[model]))
        bot.send_message(call.message.chat.id, "📥 اختر موديل جهازك لتحميل السوفت:", reply_markup=markup)

    elif call.data == "diagnose_ar":
        bot.send_message(call.message.chat.id, "🔍 أرسل رقم MAC أو موديل الجهاز وسنساعدك فورًا 🔧")

    elif call.data == "lang_en":
        bot.send_message(call.message.chat.id, "✅ English support will be added soon.")

# تشغيل البوت
bot.infinity_polling()
