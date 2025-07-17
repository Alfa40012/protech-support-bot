#!/bin/bash

echo "✅ بدء إنشاء مفتاح SSH جديد..."

# إنشاء مجلد SSH إن لم يكن موجودًا
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# إنشاء مفتاح جديد بدون باسورد
ssh-keygen -t ed25519 -C "protech-bot" -f ~/.ssh/id_ed25519 -N ""

echo ""
echo "✅ تم إنشاء مفتاح SSH بنجاح."
echo ""

# عرض المفتاح العام لنسخه
echo "⬇️ المفتاح العام الخاص بك (انسخه كاملًا):"
echo "--------------------------------------------------"
cat ~/.ssh/id_ed25519.pub
echo "--------------------------------------------------"
echo ""
echo "📌 افتح الرابط التالي وأضف المفتاح:"
echo "👉 https://github.com/settings/ssh/new"
echo ""
echo "✍️ عنوان (Title): protech-vps"
echo "📋 ثم الصق المفتاح في خانة (Key) واحفظه"
echo ""

read -p "اضغط Enter بعد إضافة المفتاح في GitHub..."

# اختبار الاتصال بـ GitHub
echo ""
echo "🔁 اختبار الاتصال بـ GitHub..."
ssh -T git@github.com

# تنزيل مستودع البوت
echo ""
echo "📥 جاري تحميل البوت من GitHub..."
cd /opt
rm -rf protech-support-bot
git clone git@github.com:Alfa40012/protech-support-bot.git

echo ""
echo "✅ تم تحميل البوت بنجاح في /opt/protech-support-bot"
echo ""
echo "👨‍💻 لتشغيل البوت: "
echo "cd /opt/protech-support-bot && python3 main.py"
