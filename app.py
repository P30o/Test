import telebot

# تعريف متغير لحفظ توكن البوت
bot_token = "7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY"

# إنشاء كائن للبوت باستخدام توكن البوت
bot = telebot.TeleBot(bot_token)

# قائمة لتخزين الصور المستقبلة
user_photos = {}

# دالة للتعامل مع الصور المرسلة من المستخدم
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    # الحصول على معرف المستخدم
    user_id = message.from_user.id
    
    # تخزين الصورة في القائمة الخاصة بالمستخدم
    if user_id not in user_photos:
        user_photos[user_id] = []
    
    # إضافة الملف إلى قائمة الصور
    user_photos[user_id].append(message.photo[-1].file_id)
    
    # تأكيد استقبال الصورة
    bot.reply_to(message, "تم استقبال الصورة!")

# دالة لإرسال آخر صورة استقبلها البوت من المستخدم
@bot.message_handler(commands=['last_photo'])
def send_last_photo(message):
    user_id = message.from_user.id
    
    if user_id in user_photos and user_photos[user_id]:
        last_photo_id = user_photos[user_id][-1]
        bot.send_photo(user_id, last_photo_id)
    else:
        bot.reply_to(message, "لا يوجد صور لإرسالها.")

# تشغيل البوت
bot.polling()
