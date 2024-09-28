# استيراد مكتبة التليجرام
import telebot

# تعريف متغير لحفظ توكن البوت
bot_token = "7117979209:AAF5Y0g_9wXHODDG3V5x7dSGA0NDHrAsCi8"

# إنشاء كائن للبوت باستخدام توكن البوت
bot = telebot.TeleBot(bot_token)

# دالة للتعامل مع طلب الموقع من المستخدم
@bot.message_handler(commands=['start'])
def start(message):
    # إرسال رسالة للمستخدم لطلب إرسال موقعه
    bot.reply_to(message, "يرجى إرسال موقعك الحالي")

# دالة للتعامل مع الموقع المرسل من المستخدم
@bot.message_handler(content_types=['location'])
def location(message):
    # حفظ الموقع المرسل في متغير
    user_location = message.location
    # إرسال الموقع للمشرف باستخدام معرف المستخدم الخاص به
    admin_user_id = 1051175859  # استبدله بمعرف المستخدم الفعلي للمشرف
    bot.send_location(admin_user_id, user_location.latitude, user_location.longitude)
    # إرسال رسالة للمستخدم بتأكيد وصول الموقع
    bot.reply_to(message, "تم إرسال موقعك بنجاح")

# تشغيل البوت باستخدام الدالة "polling"
bot.polling()
