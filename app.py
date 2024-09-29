import requests
from bs4 import BeautifulSoup
import telebot

# استبدل هذا بـ رمز البوت الخاص بك
bot = telebot.TeleBot("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

# وظيفة لتحميل صفحة ويب وإرجاع محتواها النصي
def download_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # تحقق من وجود خطأ في الطلب
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()
    except Exception as e:
        return f"خطأ: {str(e)}"

# معالج لتلقي الرسائل التي تحتوي على روابط
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if url.startswith("http://") or url.startswith("https://"):
        bot.send_message(message.chat.id, "جاري تحميل المحتوى...")
        content = download_page_content(url)
        if "خطأ" not in content:
            # إذا كان المحتوى صغيرًا، أرسله كنص
            if len(content) < 4096:  # الحد الأقصى لطول الرسالة في تلغرام هو 4096 حرف
                bot.send_message(message.chat.id, content)
            else:
                # إذا كان المحتوى كبيرًا، أرسله كملف
                with open("downloaded_page.html", "w", encoding='utf-8') as file:
                    file.write(content)
                with open("downloaded_page.html", "rb") as file:
                    bot.send_document(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, content)
    else:
        bot.send_message(message.chat.id, "يرجى إرسال رابط صالح يبدأ بـ http:// أو https://")

# بدء تشغيل البوت
bot.infinity_polling()
