from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, 
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📺 موديلات PROTECH", callback_data="models")],
        [InlineKeyboardButton("🛰️ ملفات القنوات", callback_data="channels")],
        [InlineKeyboardButton("💳 تجديد الاشتراك", url="https://wa.me/p/10036792293099711/201098256570")],
        [InlineKeyboardButton("🛒 شراء اونلاين", url="https://wa.me/c/201098256570")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 مرحبًا بك في بوت دعم أجهزة PROTECH IPTV\n\nاختر الخدمة التي تريدها من القائمة أدناه:",
        reply_markup=reply_markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "models":
        models_keyboard = [
            [InlineKeyboardButton("PROTECH 10", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
            [InlineKeyboardButton("PROTECH P10W", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
            [InlineKeyboardButton("PROTECH P04W", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
            [InlineKeyboardButton("PROTECH P08W", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
            [InlineKeyboardButton("PROTECH new1", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
            [InlineKeyboardButton("PROTECH new2", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
        ]
        await query.edit_message_text(
            "📥 اختر موديل جهازك لتحميل السوفت المناسب:",
            reply_markup=InlineKeyboardMarkup(models_keyboard)
        )

    elif query.data == "channels":
        await query.edit_message_text(
            "⚠️ *حصريًا قبل أي حد*\n\n"
            "🗓️ *أحدث ملف قنوات بتاريخ:* 2025/7/1\n"
            "✅ *لأجهزة صن بلص:* 2507L - 1507DK - 1506TV-HV\n"
            "📡 *نايل سات عربي - متحرك عربي*\n\n"
            "📺 *تم إضافة:*\n"
            "• قناة بين الإخبارية\n"
            "• قناة دوللي كلاسيك\n"
            "• قناة العاصمة الجديدة\n\n"
            "🛰️ *نايل سات عربي:*\n"
            "[تحميل مباشر](https://www.mediafire.com/file/ww5cz83z2ot5p2j/صن+بلص+داكى+نايل+سات+عربي+شهر+7.bin/file)\n\n"
            "🛰️ *متحرك عربي:*\n"
            "[تحميل مباشر](https://www.mediafire.com/file/q19ps221mcu2u73/)",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
