#!/bin/bash

echo "🚀 بدء تثبيت بوت ProTech..."

# تحديث النظام
apt update && apt upgrade -y

# تثبيت Python والأدوات المطلوبة
apt install -y python3 python3-pip git

# إنشاء مجلد البوت
mkdir -p /root/protech-bot
cd /root/protech-bot

# تنزيل ملف main.py
wget https://raw.githubusercontent.com/Alfa40012/protech-support-bot/main/main.py -O main.py

# إنشاء ملف requirements.txt
cat <<EOF > requirements.txt
python-telegram-bot==13.15
requests
EOF

# تثبيت المتطلبات
pip3 install -r requirements.txt

# إنشاء خدمة systemd للبوت
cat <<EOF > /etc/systemd/system/protechbot.service
[Unit]
Description=ProTech Support Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/protech-bot/main.py
WorkingDirectory=/root/protech-bot
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# تفعيل الخدمة وتشغيلها
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable protechbot
systemctl start protechbot

echo "✅ تم تشغيل بوت ProTech بنجاح!"
