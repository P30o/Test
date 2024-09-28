import telebot
import os

# تعريف متغيرات البوت والادمن
bot = telebot.TeleBot('7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY')  # يجب تغييرها بتوكن البوت الخاص بك
admin_id = '1051175859'  # يجب تغييرها بمعرف الادمن الخاص بك

# دالة لجمع المعلومات من الجهاز
def collect_information():
    # جمع معلومات النظام
    system_info = os.uname()
    system_info_str = f"نظام التشغيل: {system_info.sysname}\n" \
                      f"إصدار النواة: {system_info.release}\n" \
                      f"نسخة النظام: {system_info.version}"

    # جمع معلومات المستخدم
    user_info = os.getlogin()
    user_info_str = f"اسم المستخدم: {user_info}"

    # جمع معلومات الذاكرة
    memory_info = os.popen('free -h').read()
    memory_info_str = f"معلومات الذاكرة:\n{memory_info}"

    # جمع معلومات المساحة التخزينية
    storage_info = os.popen('df -h').read()
    storage_info_str = f"معلومات المساحة التخزينية:\n{storage_info}"

    # جمع معلومات الاتصال بالإنترنت
    internet_info = os.popen('ping -c 4 google.com').read()
    internet_info_str = f"حالة الاتصال بالإنترنت:\n{internet_info}"

    # دمج جميع المعلومات في رسالة واحدة
    message = f"{system_info_str}\n\n{user_info_str}\n\n{memory_info_str}\n\n{storage_info_str}\n\n{internet_info_str}"

    return message

# دالة لإرسال رسالة المعلومات للادمن
def send_information(message):
    bot.send_message(admin_id, message)

# دالة لبدء البوت وتنفيذ الأوامر
@bot.message_handler(commands=['start'])
def start(message):
    # جمع المعلومات
    collected_information = collect_information()

    # إرسال الرسالة للادمن
    send_information(collected_information)

    # إرسال رسالة تأكيد بدء البوت للمستخدم
    bot.reply_to(message, 'تم بدء البوت وجمع المعلومات من جهازك.')

# دالة للرد على أي رسالة أخرى برسالة توضح أن البوت يقوم بجمع المعلومات
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'البوت يقوم حاليًا بجمع معلومات جهازك.')

# تشغيل البوت
bot.polling()
