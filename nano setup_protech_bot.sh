#!/bin/bash

echo "🚀 بدء تثبيت بوت PROTECH IPTV..."

# 1. تحديث النظام
sudo apt update && sudo apt upgrade -y

# 2. تثبيت Python وPIP
sudo apt install python3 python3-pip -y

# 3. إنشاء مجلد البوت
mkdir -p ~/protech_bot
cd ~/protech_bot

# 4. إنشاء ملف البوت
cat <<EOF > bot.py
import telebot

BOT_TOKEN = '7579051023:AAHO56s_EMzenHUKPpuojzJf-KRKykJC10I'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📡 تفعيل IPTV', '📥 تحميل السوفت')
    markup.row('📶 ملف القنوات', '❓ تشخيص المشكلة')
    markup.row('🧑‍💻 التواصل مع الدعم', '💬 واتساب مباشر')
    bot.send_message(message.chat.id,
                     "👋 أهلاً بك في دعم PROTECH IPTV\n\nاختر من القائمة التالية 👇",
                     reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def reply_all(message):
    if message.text == '📡 تفعيل IPTV':
        bot.send_message(message.chat.id, "🔧 من فضلك أرسل نوع الجهاز واسم السيرفر المطلوب تفعيله.")
    elif message.text == '📥 تحميل السوفت':
        bot.send_message(message.chat.id, "📦 حمل آخر سوفت من هنا:\nhttps://www.mediafire.com/folder/...")  # غيّر الرابط
    elif message.text == '📶 ملف القنوات':
        bot.send_message(message.chat.id, "🛰️ حمل ملف القنوات نايل سات:\nhttps://www.mediafire.com/file/vm2khd0dnemy7ro/...")
    elif message.text == '❓ تشخيص المشكلة':
        bot.send_message(message.chat.id, "💡 من فضلك أرسل نوع الجهاز والمشكلة بالتفصيل.")
    elif message.text == '🧑‍💻 التواصل مع الدعم':
        bot.send_message(message.chat.id, "🎧 تواصل مع الدعم عبر Telegram: @ProTechSupport1")
    elif message.text == '💬 واتساب مباشر':
        bot.send_message(message.chat.id, "📲 تواصل معنا عبر واتساب:\nhttps://wa.me/message/2JZ4HHC5JOSFC1")
    else:
        bot.send_message(message.chat.id, "❗ لم أفهم الأمر، يرجى اختيار من القائمة.")

bot.polling(none_stop=True)
EOF

# 5. إنشاء ملف تشغيل تلقائي باستخدام systemd
sudo tee /etc/systemd/system/protechbot.service > /dev/null <<EOL
[Unit]
Description=ProTech IPTV Support Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/$USER/protech_bot/bot.py
WorkingDirectory=/home/$USER/protech_bot
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOL

# 6. تفعيل الخدمة
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable protechbot
sudo systemctl start protechbot

echo "✅ تم تشغيل بوت PROTECH IPTV بنجاح 🎉"
