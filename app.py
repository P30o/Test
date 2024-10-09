import os
import subprocess
import shutil
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pathlib import Path

# توكن بوت التليجرام
TELEGRAM_BOT_TOKEN = "7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY"

# المجلد الذي سيتم حفظ المواقع فيه
OUTPUT_DIR = "/path/to/save/websites"

def download_website(website_url: str, output_dir: str) -> bool:
    """تنفيذ wget لتحميل الموقع."""
    command = [
        'wget',
        '--mirror',
        '--convert-links',
        '--adjust-extension',
        '--page-requisites',
        '--no-parent',
        '--directory-prefix=' + output_dir,
        website_url
    ]

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def zip_directory(directory: str, zip_name: str) -> str:
    """ضغط المجلد وتحويله إلى ملف ZIP."""
    shutil.make_archive(zip_name, 'zip', directory)
    return zip_name + ".zip"

def start(update: Update, context: CallbackContext) -> None:
    """الرد على أمر /start."""
    update.message.reply_text('مرحباً! أرسل لي رابط الموقع الذي تريد تحميله.')

def download_command(update: Update, context: CallbackContext) -> None:
    """تنفيذ أمر التحميل عند استقبال رابط."""
    if context.args:
        website_url = context.args[0]
        update.message.reply_text(f"جارٍ تحميل الموقع: {website_url}")
        
        # اسم المجلد لحفظ الموقع
        folder_name = Path(website_url).netloc
        full_output_path = os.path.join(OUTPUT_DIR, folder_name)
        
        # تحميل الموقع
        if download_website(website_url, full_output_path):
            # ضغط الموقع
            zip_file_path = zip_directory(full_output_path, full_output_path)
            message = "✅ تم تحميل الموقع وضغطه بنجاح! جاري إرسال الملف..."
            
            # إرسال ملف ZIP للمستخدم
            with open(zip_file_path, 'rb') as zip_file:
                update.message.reply_document(document=zip_file, filename=f"{folder_name}.zip")
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
