import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# دالة لجلب محتوى الموقع
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)

# دالة للتعامل مع أمر /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "مرحبًا! أرسل لي رابط الموقع وسأقوم بسحب محتواه."
    )

# دالة للتعامل مع الرسائل
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    content = fetch_website_content(url)

    if "Exception" in content:
        update.message.reply_text("حدث خطأ: " + content)
        return

    # حفظ المحتوى في ملف
    with open('website_content.html', 'w', encoding='utf-8') as file:
        file.write(content)

    # إرسال الملف إلى المستخدم
    with open('website_content.html', 'rb') as file:
        update.message.reply_document(file, caption="إليك محتوى الموقع!")

def main():
    # استبدل 'YOUR_TOKEN' برمز البوت الخاص بك
    updater = Updater('7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))  # إضافة معالجة لأمر /start
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
