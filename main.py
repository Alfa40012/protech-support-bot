import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# بيانات البوت
API_TOKEN = '7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I'

# إعدادات اللوج
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ====== لوحة التحكم الأساسية ======
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📥 تحميل السوفت", callback_data="soft"),
        InlineKeyboardButton("📡 ملف قنوات نايل سات", callback_data="channels"),
        InlineKeyboardButton("💳 تفعيل IPTV", callback_data="iptv"),
        InlineKeyboardButton("🛠 دعم فني مباشر", callback_data="support"),
        InlineKeyboardButton("📞 تواصل واتساب", url="https://wa.me/message/2JZ4HHC5JOSFC1"),
    )
    return kb

# ====== رسالة ترحيب أول مرة ======
@dp.message_handler(commands=["start"])
async def start_cmd(message: Message):
    await message.answer("👋 مرحبًا بك في بوت الدعم الفني PROTECH.\nاختر من القائمة:", reply_markup=main_menu())

@dp.message_handler()
async def on_any_text(message: types.Message):
    text = message.text.strip()

    if len(text) == 12 and ":" not in text and text.upper().startswith("00"):
        await message.reply(f"✅ تم استقبال MAC: `{text}` بنجاح.\nسيتم الرد عليك قريبًا.", parse_mode="Markdown")
    elif any(x in text.lower() for x in ["استرا", "سالكوم", "تايجر", "جي اكس", "h265", "h1", "gx", "xtream", "iptv"]):
        await message.reply("📌 تم تحديد نوع الجهاز.\nيرجى الآن كتابة اسم السيرفر أو إرسال MAC.")
    else:
        await message.reply("📋 اختر الخدمة التي تحتاجها من القائمة:", reply_markup=main_menu())

# ====== الضغط على الأزرار ======
@dp.callback_query_handler(lambda c: True)
async def on_callback(callback: types.CallbackQuery):
    data = callback.data

    if data == "soft":
        await callback.message.answer("📥 اختر نوع جهازك لتحميل السوفت.\n(مستقبلاً سيتم التحديد تلقائيًا)")
    elif data == "channels":
        await callback.message.answer_document(
            types.InputFile.from_url("https://www.mediafire.com/file/vm2khd0dnemy7ro/file"),
            caption="✅ تم إرسال ملف القنوات (نايل سات) بنجاح."
        )
    elif data == "iptv":
        await callback.message.answer("💳 من فضلك اكتب نوع الجهاز + اسم السيرفر المراد التفعيل عليه.")
    elif data == "support":
        await callback.message.answer("🛠 فريق الدعم الفني جاهز لخدمتك.\nيرجى إرسال المشكلة أو MAC الخاص بجهازك.")
    await callback.answer()

# ====== تشغيل البوت ======
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
