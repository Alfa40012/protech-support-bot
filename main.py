import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters, ConversationHandler
)
import sqlite3
import asyncio

# --- إعدادات اللوق ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ضع توكن البوت هنا ---
BOT_TOKEN = "7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I"

# --- مراحل الـ ConversationHandler ---
(
    LANG_CHOOSE, MAIN_MENU, SOFT_TYPE, IPTV_DEVICE,
    IPTV_SERVER, IPTV_MAC, DIAG_PROBLEM, DIAG_DEVICE,
    DIAG_MAC
) = range(9)

# --- قاعدة بيانات SQLite ---
conn = sqlite3.connect("protech_support.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        language TEXT DEFAULT 'ar'
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        ticket_type TEXT,
        device TEXT,
        server TEXT,
        mac TEXT,
        problem TEXT,
        language TEXT,
        status TEXT DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        active INTEGER DEFAULT 1
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        active INTEGER DEFAULT 1
    )
    ''')
    conn.commit()

init_db()

# --- روابط السوفت حسب الجهاز ---
SOFT_FILES = {
    "Z": "https://mediafire.com/soft_z",
    "Nova": "https://mediafire.com/soft_nova",
    "StarSat": "https://mediafire.com/soft_starsat",
}

IPTV_SERVERS = ["Nova", "Aroma", "Protech"]

SUPPORT_CHANNEL_ID = -1001234567890  # عوضا عن معرف قناتك أو تيليجرام خاص

WA_LINK = "https://wa.me/message/2JZ4HHC5JOSFC1"

FAQ_LIST = [
    {"question": "كيف يمكنني تفعيل الاشتراك؟",
     "answer": "يرجى إرسال نوع جهازك، السيرفر، ورقم الماك عبر البوت."},
    {"question": "ماذا أفعل إذا توقفت القنوات عن العمل؟",
     "answer": "جرب إعادة تشغيل الجهاز والتأكد من اتصال الإنترنت."},
    {"question": "كيف أحصل على تحديث السوفت؟",
     "answer": "اختر خيار تحميل السوفت من قائمة البوت."},
]

MESSAGES = {
    "ar": {
        "welcome": "مرحبًا بك في بوت دعم PROTECH IPTV 👋\nاختر لغتك:",
        "choose_language": "اختر لغتك:",
        "main_menu": "القائمة الرئيسية:",
        "choose_soft": "اختر نوع جهازك لتحميل السوفت:",
        "send_soft": "رابط تحميل السوفت لجهازك:\n{}",
        "channels": "ملف القنوات العربي (نايل سات) جاهز للتحميل.",
        "send_channels": "🔗 اضغط لتحميل ملف القنوات (رابط مخفي).",
        "iptv_device": "ما نوع جهازك؟",
        "iptv_server": "ما اسم السيرفر الذي تريد التفعيل عليه؟",
        "iptv_mac": "أرسل رقم الماك (MAC Address) الخاص بجهازك:",
        "iptv_confirm": "جارٍ تحويل طلبك لفريق التفعيل، سيتم الرد خلال دقائق.",
        "diag_problem": "ما نوع المشكلة التي تواجهها؟",
        "diag_device": "أرسل نوع جهازك:",
        "diag_mac": "أرسل رقم الماك الخاص بجهازك:",
        "diag_confirm": "شكراً، جاري إرسال طلب التشخيص لفريق الدعم.",
        "support_contact": "للتواصل مع الدعم الفني عبر واتساب، اضغط الزر أدناه:",
        "offers_title": "العروض والخصومات الحالية:",
        "faq_title": "الأسئلة الشائعة:",
        "back_menu": "عودة إلى القائمة الرئيسية",
        "invalid_option": "خيار غير صالح، حاول مرة أخرى.",
        "ticket_created": "تم إنشاء تذكرتك رقم #{}، وسنوافيك بالرد قريبًا.",
    },
    "en": {
        "welcome": "Welcome to PROTECH IPTV Support Bot 👋\nChoose your language:",
        "choose_language": "Choose your language:",
        "main_menu": "Main Menu:",
        "choose_soft": "Select your device type to download software:",
        "send_soft": "Here is your software download link:\n{}",
        "channels": "Arabic Channels file (NileSat) ready for download.",
        "send_channels": "🔗 Click to download channels file (hidden link).",
        "iptv_device": "What is your device type?",
        "iptv_server": "Which server do you want to activate on?",
        "iptv_mac": "Please send your MAC Address:",
        "iptv_confirm": "Your activation request is being forwarded to the activation team. You'll be contacted shortly.",
        "diag_problem": "What problem are you facing?",
        "diag_device": "Send your device type:",
        "diag_mac": "Send your MAC Address:",
        "diag_confirm": "Thanks, your diagnostic request has been sent to the support team.",
        "support_contact": "To contact support via WhatsApp, click the button below:",
        "offers_title": "Current Offers and Discounts:",
        "faq_title": "Frequently Asked Questions:",
        "back_menu": "Back to Main Menu",
        "invalid_option": "Invalid option, please try again.",
        "ticket_created": "Your ticket #{} has been created, we'll respond soon.",
    },
}

# --- دوال مساعدة ---

def get_user_language(user_id: int):
    cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return "ar"

def set_user_language(user_id: int, lang: str):
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, lang)
    )
    conn.commit()

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_language(update.effective_user.id)
    text = MESSAGES[lang]["main_menu"]
    keyboard = [
        [
            InlineKeyboardButton("📥 تحميل السوفت", callback_data="menu_soft"),
            InlineKeyboardButton("📺 ملف القنوات", callback_data="menu_channels"),
        ],
        [InlineKeyboardButton("🎯 تفعيل الاشتراك IPTV", callback_data="menu_iptv")],
        [
            InlineKeyboardButton("📝 تشخيص المشكلة / فحص الكود", callback_data="menu_diag")
        ],
        [
            InlineKeyboardButton("🔧 الدعم الفني", callback_data="menu_support"),
            InlineKeyboardButton("💬 تواصل واتساب", url=WA_LINK),
        ],
        [InlineKeyboardButton("📢 العروض والخصومات", callback_data="menu_offers")],
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="menu_faq")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("العربية", callback_data="lang_ar")],
        [InlineKeyboardButton("English", callback_data="lang_en")],
    ]
    await update.message.reply_text(
        MESSAGES["ar"]["welcome"], reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split("_")[1]
    user_id = query.from_user.id
    set_user_language(user_id, lang_code)
    text = {
        "ar": "تم اختيار اللغة العربية ✅",
        "en": "English language selected ✅",
    }[lang_code]
    await query.edit_message_text(text)
    # أرسل المنيو الرئيسي
    chat_id = query.message.chat.id
    keyboard = [
        [
            InlineKeyboardButton("📥 تحميل السوفت", callback_data="menu_soft"),
            InlineKeyboardButton("📺 ملف القنوات", callback_data="menu_channels"),
        ],
        [InlineKeyboardButton("🎯 تفعيل الاشتراك IPTV", callback_data="menu_iptv")],
        [
            InlineKeyboardButton("📝 تشخيص المشكلة / فحص الكود", callback_data="menu_diag")
        ],
        [
            InlineKeyboardButton("🔧 الدعم الفني", callback_data="menu_support"),
            InlineKeyboardButton("💬 تواصل واتساب", url=WA_LINK),
        ],
        [InlineKeyboardButton("📢 العروض والخصومات", callback_data="menu_offers")],
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="menu_faq")],
    ]
    await context.bot.send_message(
        chat_id=chat_id, text=MESSAGES[lang_code]["main_menu"], reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text
