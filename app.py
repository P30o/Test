import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# توكن بوت التليجرام
TELEGRAM_BOT_TOKEN = "7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY"

# المجلد الذي سيتم حفظ الموقع فيه
OUTPUT_DIR = "/path/to/save/websites"

def download_website(website_url):
    """تنفذ أمر wget لتحميل الموقع."""
    command = f'wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --directory-prefix={OUTPUT_DIR} {website_url}'
    result = os.system(command)
    return result == 0

def start(update: Update, context: CallbackContext) -> None:
    """الرد على أمر /start."""
    update.message.reply_text('مرحباً! أرسل لي رابط الموقع الذي تريد تحميله.')

def download_command(update: Update, context: CallbackContext) -> None:
    """تنفيذ أمر التحميل عند استقبال رابط."""
    if context.args:
        website_url = context.args[0]
        update.message.reply_text(f"جارٍ تحميل الموقع: {website_url}")
        
        # تحميل الموقع
        if download_website(website_url):
            message = f"✅ تم تحميل الموقع بنجاح!"
        else:
            message = "❌ حدث خطأ أثناء تحميل الموقع."
        
        # إرسال نتيجة التحميل
        update.message.reply_text(message)
    else:
        update.message.reply_text("❌ يرجى إرسال رابط صالح.")

def main():
    """تشغيل البوت."""
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    # الحصول على الـ Dispatcher لتسجيل الأوامر
    dispatcher = updater.dispatcher

    # تسجيل الأوامر
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("download", download_command))

    # بدء البوت
    updater.start_polling()

    # إبقاء البوت مستمراً حتى يتم إيقافه
    updater.idle()

if __name__ == '__main__':
    main()
