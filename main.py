from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

# بيانات البوت
TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"
ADMIN_ID = 907876903
WELCOME_IMAGE = "https://g.top4top.io/p_3486pis4c0.jpg"
WHATSAPP_LINK = "https://wa.me/message/2JZ4HHC5JOSFC1"

# إعداد البوت
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# لوحة المفاتيح
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("🧰 الدعم الفني", "🧾 موديلات الأجهزة")
main_menu.add("📥 السوفت وير", "📺 ملف القنوات")
main_menu.add("🛒 طلب اشتراك", "🌐 موقع بروتيك")

# رسالة الترحيب
welcome_caption = """
<b>🎉 أهلاً بك في بوت بروتيك لخدمات الدعم</b>
مرحباً بك داخل وخارج مصر، معك Support مباشر 💬

🛠 خدماتنا تشمل:
• الدعم الفني
• موديلات الأجهزة
• السوفت وير
• ملفات القنوات
• طلب اشتراك مباشر
• الموقع الرسمي

<b>👇 اختر الخدمة المطلوبة من القائمة أدناه</b>

<b>Welcome to ProTech Support</b>
We support all users in and outside Egypt 🌍

⚙️ Choose from the menu below 👇
"""

# عند بدء المحادثة
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=WELCOME_IMAGE,
        caption=welcome_caption,
        reply_markup=main_menu,
        parse_mode="HTML"
    )

# الردود على الخيارات
@dp.message_handler()
async def handle_buttons(message: types.Message):
    text = message.text.strip()

    if text == "🧰 الدعم الفني":
        await message.reply("🔧 للدعم الفني، تواصل معنا عبر واتساب:\n" + WHATSAPP_LINK)
    elif text == "🧾 موديلات الأجهزة":
        await message.reply("📋 قائمة الموديلات المتوفرة على موقع بروتيك:\n🌐 https://protech-eg.com/models")
    elif text == "📥 السوفت وير":
        await message.reply("⬇️ لتحميل السوفت، زر موقعنا:\n🌐 https://protech-eg.com/firmware")
    elif text == "📺 ملف القنوات":
        await message.reply("📡 حمل ملف القنوات الأحدث من هنا:\n🌐 https://protech-eg.com/channels")
    elif text == "🛒 طلب اشتراك":
        await message.reply("🛍 لطلب الاشتراك أو التجربة:\n📱 واتساب: " + WHATSAPP_LINK)
    elif text == "🌐 موقع بروتيك":
        await message.reply("🌐 تفضل بزيارة موقعنا الرسمي:\nhttps://protech-eg.com")
    else:
        await message.reply(f"""❗ عذرًا، لم أفهم اختيارك

📱 للتواصل المباشر عبر واتساب:
{WHATSAPP_LINK}
""")

# بدء التنفيذ
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
