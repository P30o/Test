   import os
   from pywebcopy import save_webpage
   import telebot

   # استبدل هذا بـ رمز البوت الخاص بك
   bot = telebot.TeleBot("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

   # مسار حفظ الملفات
   DOWNLOAD_FOLDER = "downloaded_sites"

   if not os.path.exists(DOWNLOAD_FOLDER):
       os.makedirs(DOWNLOAD_FOLDER)

   # وظيفة لتحميل الموقع بالكامل
   def download_full_site(url, download_folder):
       try:
           kwargs = {'bypass_robots': True, 'project_name': 'site_copy'}
           save_webpage(url, download_folder, **kwargs)
           return os.path.join(download_folder, 'site_copy')
       except Exception as e:
           return f"خطأ: {str(e)}"

   # معالج لتلقي الرسائل التي تحتوي على روابط
   @bot.message_handler(func=lambda message: True)
   def handle_message(message):
       url = message.text
       if url.startswith("http://") or url.startswith("https://"):
           bot.send_message(message.chat.id, "جاري تحميل الموقع بالكامل...")
           download_path = download_full_site(url, DOWNLOAD_FOLDER)
           if not download_path.startswith("خطأ"):
               zip_name = f"{download_path}.zip"
               os.system(f"zip -r {zip_name} {download_path}")
               with open(zip_name, "rb") as file:
                   bot.send_document(message.chat.id, file)
               os.remove(zip_name)  # حذف الملف المضغوط بعد الإرسال
           else:
               bot.send_message(message.chat.id, download_path)
       else:
           bot.send_message(message.chat.id, "يرجى إرسال رابط صالح يبدأ بـ http:// أو https://")

   # بدء تشغيل البوت
   bot.infinity_polling()
   