from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "توكن_البوت_هنا"

# --- الردود المنسقة ---
WELCOME_MSG = """*👋 مرحبًا بك في بوت الدعم الفني لـ PROTECH IPTV*

*🤖 البوت يعمل تلقائيًا وعلى مدار الساعة لخدمتك.*

📡 إذا واجهت أي *مشكلة* أو كنت بحاجة إلى *مساعدة*:

✅ اختر من القائمة بالأسفل  
✅ أو اكتب *اسم جهازك*  
✅ أو أرسل *كود MAC* الخاص بجهازك

🔧 *نحن هنا لمساعدتك بكل احترافية!*"""

CHANNELS_MSG = """⚠️ *حصــــــرياً وقبل أي حـــــد* ⚠️
*ملف قنــــــوات صن بلـــــص الأســـــطوري*
2507L - 1507DK - 1506TV-HV

📡 *تحديث ناري بكل جديد على جميع الأقمار*
*وأحدث القنوات على نايل سات 2025*

✅ *الأنظمة المدعومة:*
✔️ نايل سات عربي ثابت  
✔️ متحرك عربي لجميع الاتجاهات

◀️ *تمت إضافة القنوات الجديدة بالتحديث:*
✨ قناة العاصمة الجديدة — جودة ممتازة  
✨ قناة الثانية HD — نقاء غير مسبوق  
✨ مصر دراما MBC — لكل عشاق الدراما

🔻 *ملف نايل سات عربي:*  
🔗 https://www.up-4ever.net/c3subfw3rmvv

🔻 *ملف متحرك عربي:*  
🔗 https://www.up-4ever.net/57bdh63208k7

⏳ *نزّل التحديث قبل الكل وكن دائمًا سابق بخطوة!*"""

SOFTWARE_OPTIONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔽 بروتيك P10W", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
    [InlineKeyboardButton("🔽 بروتيك P10", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
    [InlineKeyboardButton("🔽 بروتيك P04W", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
    [InlineKeyboardButton("🔽 بروتيك P08W", url="https://www.mediafire.com/folder/9jv31ni4w4ayy/PROTECH")],
])

MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("📡 فحص الكود / الدعم الفني", callback_data="support")],
    [InlineKeyboardButton("📥 تحميل ملف القنوات", callback_data="channels")],
    [InlineKeyboardButton("⬇️ تحميل السوفت وير", callback_data="software")],
    [InlineKeyboardButton("💳 تجديد الاشتراك", url="https://wa.me/p/10036792293099711/201098256570")],
    [InlineKeyboardButton("🛒 شراء الأجهزة أونلاين", url="https://wa.me/c/201098256570")],
    [InlineKeyboardButton("💬 التواصل مع الدعم — واتساب", url="https://wa.me/201098256570")],
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MSG, parse_mode="Markdown", reply_markup=MAIN_MENU)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "support":
        # تحويل مباشر إلى واتساب
        await query.message.reply_text("💬 تواصل الآن مع الدعم الفني عبر واتساب:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📲 اضغط هنا", url="https://wa.me/201098256570")]
        ]))
    elif query.data == "channels":
        await query.message.reply_text(CHANNELS_MSG, parse_mode="Markdown")
    elif query.data == "software":
        await query.message.reply_text("⬇️ اختر موديل جهازك لتحميل السوفت وير المناسب:", reply_markup=SOFTWARE_OPTIONS)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()
