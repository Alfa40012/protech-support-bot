import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, ConversationHandler
)
import sqlite3
import asyncio

# --- إعداد اللوقينج ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ثوابت المراحل في ConversationHandler ---
LANGUAGE, MAIN_MENU, SOFT_TYPE, SEND_SOFT, CHANNELS, SEND_CHANNELS, \
IPTV_DEVICE, IPTV_SERVER, IPTV_MAC, IPTV_CONFIRM, \
DIAG_PROBLEM, DIAG_DEVICE, DIAG_MAC, DIAG_CONFIRM, \
SHOW_OFFERS, FAQ_MENU, SUPPORT_TICKET, = range(16)

# --- قاعدة بيانات SQLite بسيطة ---
conn = sqlite3.connect('protech_support.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        type TEXT,
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
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        language TEXT DEFAULT 'ar'
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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        active INTEGER DEFAULT 1
    )
    ''')
    conn.commit()

init_db()

# --- بيانات ثابتة (يمكن تعديلها لاحقًا من لوحة تحكم ويب) ---
SOFT_FILES = {
    'Z': 'https://mediafire.com/soft_z',
    'Nova': 'https://mediafire.com/soft_nova',
    'StarSat': 'https://mediafire.com/soft_starsat',
}

IPTV_SERVERS = ['Nova', 'Aroma', 'Protech']

SUPPORT_CHANNEL_ID = -1001234567890  # عوضاً عن معرف قناة الدعم الخاصة بك

WA_LINK = "https://wa.me/message/2JZ4HHC5JOSFC1"

# --- قائمة الأسئلة الشائعة (FAQ) ---
FAQ_LIST = [
    {
        "question": "كيف يمكنني تفعيل الاشتراك؟",
        "answer": "يرجى إرسال نوع جهازك، السيرفر، ورقم الماك عبر البوت."
    },
    {
        "question": "ماذا أفعل إذا توقفت القنوات عن العمل؟",
        "answer": "جرب إعادة تشغيل الجهاز والتأكد من اتصال الإنترنت."
    },
    {
        "question": "كيف أحصل على تحديث السوفت؟",
        "answer": "اختر خيار تحميل السوفت من قائمة البوت."
    },
]

# --- رسائل متعددة اللغات ---
MESSAGES = {
    'ar': {
        'welcome': "مرحبًا بك في بوت دعم PROTECH IPTV 👋\nاختر اللغة / Please choose your language:",
        'choose_language': "اختر لغتك:",
        'main_menu': "القائمة الرئيسية:",
        'choose_soft': "اختر نوع جهازك لتحميل السوفت:",
        'send_soft': "رابط تحميل السوفت لجهازك:\n{}",
        'channels': "ملف القنوات العربي (نايل سات) جاهز للتحميل.",
        'send_channels': "🔗 اضغط لتحميل ملف القنوات (رابط مخفي).",
        'iptv_device': "ما نوع جهازك؟",
        'iptv_server': "ما اسم السيرفر الذي تريد التفعيل عليه؟",
        'iptv_mac': "أرسل رقم الماك (MAC Address) الخاص بجهازك:",
        'iptv_confirm': "جارٍ تحويل طلبك لفريق التفعيل، سيتم الرد خلال دقائق.",
        'diag_problem': "ما نوع المشكلة التي تواجهها؟",
        'diag_device': "أرسل نوع جهازك:",
        'diag_mac': "أرسل رقم الماك الخاص بجهازك:",
        'diag_confirm': "شكراً، جاري إرسال طلب التشخيص لفريق الدعم.",
        'support_contact': "للتواصل مع الدعم الفني عبر واتساب، اضغط الزر أدناه:",
        'offers_title': "العروض والخصومات الحالية:",
        'faq_title': "الأسئلة الشائعة:",
        'back_menu': "عودة إلى القائمة الرئيسية",
        'thank_you': "شكرًا لتواصلك معنا!",
        'invalid_option': "خيار غير صالح، حاول مرة أخرى.",
        'ticket_created': "تم إنشاء تذكرتك رقم #{}، وسنوافيك بالرد قريبًا.",
        'notify_staff': "طلب دعم جديد من {} ({}). نوع الطلب: {}",
    },
    'en': {
        'welcome': "Welcome to PROTECH IPTV Support Bot 👋\nChoose your language:",
        'choose_language': "Choose your language:",
        'main_menu': "Main Menu:",
        'choose_soft': "Select your device type to download software:",
        'send_soft': "Here is your software download link:\n{}",
        'channels': "Arabic Channels file (NileSat) ready for download.",
        'send_channels': "🔗 Click to download channels file (hidden link).",
        'iptv_device': "What is your device type?",
        'iptv_server': "Which server do you want to activate on?",
        'iptv_mac': "Please send your MAC Address:",
        'iptv_confirm': "Your activation request is being forwarded to the activation team. You'll be contacted shortly.",
        'diag_problem': "What problem are you facing?",
        'diag_device': "Send your device type:",
        'diag_mac': "Send your MAC Address:",
        'diag_confirm': "Thanks, your diagnostic request has been sent to the support team.",
        'support_contact': "To contact support via WhatsApp, click the button below:",
        'offers_title': "Current Offers and Discounts:",
        'faq_title': "Frequently Asked Questions:",
        'back_menu': "Back to Main Menu",
        'thank_you': "Thank you for contacting us!",
        'invalid_option': "Invalid option, please try again.",
        'ticket_created': "Your ticket #{} has been created, we'll respond soon.",
        'notify_staff': "New support request from {} ({}). Request type: {}",
    }
}

# -- دوال مساعدة --
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_language(update.effective_user.id)
    text = MESSAGES[lang]['main_menu']
    keyboard = [
        [InlineKeyboardButton("📥 تحميل السوفت", callback_data='menu_soft'),
         InlineKeyboardButton("📺 ملف القنوات", callback_data='menu_channels')],
        [InlineKeyboardButton("🎯 تفعيل الاشتراك IPTV", callback_data='menu_iptv')],
        [InlineKeyboardButton("📝 تشخيص المشكلة / فحص الكود", callback_data='menu_diag')],
        [InlineKeyboardButton("🔧 الدعم الفني", callback_data='menu_support'),
         InlineKeyboardButton("💬 تواصل واتساب", url=WA_LINK)],
        [InlineKeyboardButton("📢 العروض والخصومات", callback_data='menu_offers')],
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='menu_faq')],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

def get_user_language(user_id: int) -> str:
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        # Default Arabic
        return 'ar'

async def set_user_language(user_id: int, language: str):
    cursor.execute('INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)', (user_id, language))
    conn.commit()

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Send language choice
    keyboard = [
        [InlineKeyboardButton("العربية", callback_data='lang_ar')],
        [InlineKeyboardButton("English", callback_data='lang_en')],
    ]
    await update.message.reply_text(MESSAGES['ar']['welcome'], reply_markup=InlineKeyboardMarkup(keyboard))

async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split('_')[1]
    user_id = query.from_user.id
    await set_user_language(user_id, lang_code)
    text = {
        'ar': "تم اختيار اللغة العربية ✅",
        'en': "English language selected ✅"
    }[lang_code]
    await query.edit_message_text(text)
    # إرسال المنيو الرئيسي
    # نستدعي send_main_menu مع رسالة جديدة
    # لا يمكن استدعاء send_main_menu مع نفس الكائن query، لذا نرسل رسالة جديدة
    chat_id = query.message.chat.id
    await context.bot.send_message(chat_id=chat_id, text=MESSAGES[lang_code]['main_menu'],
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton("📥 تحميل السوفت", callback_data='menu_soft'),
                                        InlineKeyboardButton("📺 ملف القنوات", callback_data='menu_channels')],
                                       [InlineKeyboardButton("🎯 تفعيل الاشتراك IPTV", callback_data='menu_iptv')],
                                       [InlineKeyboardButton("📝 تشخيص المشكلة / فحص الكود", callback_data='menu_diag')],
                                       [InlineKeyboardButton("🔧 الدعم الفني", callback_data='menu_support'),
                                        InlineKeyboardButton("💬 تواصل واتساب", url=WA_LINK)],
                                       [InlineKeyboardButton("📢 العروض والخصومات", callback_data='menu_offers')],
                                       [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='menu_faq')],
                                   ]))


# تظهر المنيو تلقائي لأي رسالة غير /start
async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and not update.message.text.startswith('/'):
        lang = get_user_language(update.effective_user.id)
        text = MESSAGES[lang]['main_menu']
        keyboard = [
            [InlineKeyboardButton("📥 تحميل السوفت", callback_data='menu_soft'),
             InlineKeyboardButton("📺 ملف القنوات", callback_data='menu_channels')],
            [InlineKeyboardButton("🎯 تفعيل الاشتراك IPTV", callback_data='menu_iptv')],
            [InlineKeyboardButton("📝 تشخيص المشكلة / فحص الكود", callback_data='menu_diag')],
            [InlineKeyboardButton("🔧 الدعم الفني", callback_data='menu_support'),
             InlineKeyboardButton("💬 تواصل واتساب", url=WA_LINK)],
            [InlineKeyboardButton("📢 العروض والخصومات", callback_data='menu_offers')],
            [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='menu_faq')],
        ]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# --- Callback Queries handler ---
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    lang = get_user_language(user_id)

    if data == 'menu_soft':
        # اطلب نوع الجهاز
        keyboard = [[InlineKeyboardButton(name, callback_data=f'soft_{name}') for name in SOFT_FILES.keys()]]
        keyboard.append([InlineKeyboardButton(MESSAGES[lang]['back_menu'], callback_data='back_main')])
        await query.edit_message_text(MESSAGES[lang]['choose_soft'], reply_markup=InlineKeyboardMarkup(keyboard))
        return SOFT_TYPE

    elif data.startswith('soft_'):
        soft_name = data.split('_')[1]
        link = SOFT_FILES.get(soft_name, None)
        if link:
            await query.edit_message_text(MESSAGES[lang]['send_soft'].format(link))
        else:
            await query.edit_message_text(MESSAGES[lang]['invalid_option'])
        # رجوع للمنيو
        await asyncio.sleep(1)
        await send_main_menu(update, context)
        return MAIN_MENU

    elif data == 'menu_channels':
        # إرسال رسالة ملف القنوات (رابط مخفي)
        await query.edit_message_text(MESSAGES[lang]['channels'])
        # ممكن تضيف زر تحميل ب InlineKeyboardButton مع رابط مخفي
        keyboard = [[InlineKeyboardButton("تحميل ملف القنوات", url="https://mediafire.com/fakechannelfile")]]
        keyboard.append([InlineKeyboardButton(MESSAGES[lang]['back_menu'], callback_data='back_main')])
        await query.edit_message_text(MESSAGES[lang]['channels'], reply_markup=InlineKeyboardMarkup(keyboard))
        return MAIN_MENU

    elif data == 'menu_iptv':
        # بدء فورم التفعيل
        await query.edit_message_text(MESSAGES[lang]['iptv_device'])
        return IPTV_DEVICE

    elif data == 'menu_diag':
        await query.edit_message_text(MESSAGES[lang]['diag_problem'])
        return DIAG_PROBLEM

    elif data == 'menu_support':
        keyboard = [[InlineKeyboardButton("💬 تواصل واتساب", url=WA_LINK)],
                    [InlineKeyboardButton(MESSAGES[lang]['back_menu'], callback_data='back_main')]]
        await query.edit_message_text(MESSAGES[lang]['support_contact'], reply_markup=InlineKeyboardMarkup(keyboard))
        return MAIN_MENU

    elif data == 'menu_offers':
        # عرض العروض من قاعدة البيانات
        cursor.execute("SELECT title, description FROM offers WHERE active=1")
        offers = cursor.fetchall()
        if offers:
            msg = MESSAGES[lang]['offers_title'] + "\n\n"
            for title, desc in offers:
                msg += f"⭐ {title}\n{desc}\n\n"
        else:
            msg = "لا توجد عروض حالياً." if lang == 'ar' else "No offers currently."
        keyboard = [[InlineKeyboardButton(MESSAGES[lang]['back_menu'], callback_data='back_main')]]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        return MAIN_MENU

    elif data == 'menu_faq':
        # عرض الأسئلة الشائعة
        msg = MESSAGES[lang]['faq_title'] + "\n\n"
        for i, faq in enumerate(FAQ_LIST, 1):
            msg += f"{i}. {faq['question']}\n   ➡️ {faq['answer']}\n\n"
        keyboard = [[InlineKeyboardButton(MESSAGES[lang]['back_menu'], callback_data='back_main')]]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        return MAIN_MENU

    elif data == 'back_main':
        # رجوع للمنيو الرئيسي
        text = MESSAGES[lang]['main_menu']
        keyboard = [
            [InlineKeyboardButton("📥 تحميل السوفت", callback_data='menu_soft'),
             InlineKeyboardButton("📺 ملف القنوات", callback_data='menu_channels')],
            [InlineKeyboardButton("🎯 تفعيل الاشتراك IPTV", callback_data='menu_iptv')],
            [InlineKeyboardButton("📝 تشخيص المشكلة / فحص الكود", callback_data='menu_diag')],
            [InlineKeyboardButton("🔧 الدعم الفني", callback_data='menu_support'),
             InlineKeyboardButton("💬 تواصل واتساب", url=WA_LINK)],
            [InlineKeyboardButton("📢 العروض والخصومات", callback_data='menu_offers')],
            [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='menu_faq')],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return MAIN_MENU

    else:
        await query.edit_message_text(MESSAGES[lang]['invalid_option'])
        return MAIN_MENU

# --- فورم التفعيل IPTV ---

async def iptv_device_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    context.user_data['iptv_device'] = text
    await update.message.reply_text(MESSAGES[lang]['iptv_server'])
    return IPTV_SERVER

async def iptv_server_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message
