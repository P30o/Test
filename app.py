import requests
import telebot
from telebot import types

# ضع توكن البوت الخاص بك هنا
bot_token = "7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY"
bot = telebot.TeleBot(bot_token)

# زر Inline لإجراء الفحص
btn1 = types.InlineKeyboardButton(text='🔍 تحقق من IP', callback_data='check')

@bot.message_handler(commands=["start"])
def start(message):
    # إنشاء لوحة المفاتيح مع الزر
    brok = types.InlineKeyboardMarkup()
    brok.row_width = 2
    brok.add(btn1)
    
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f'''
**
مرحباً بك - [{first_name}](tg://settings)
في بوت معلومات الـ IP.
أرسل الـ IP الذي ترغب في معرفة معلوماته وانتظر...
**''', parse_mode='Markdown', reply_markup=brok)

@bot.callback_query_handler(func=lambda call: call.data == 'check')
def ip(call):
    bot.send_message(call.message.chat.id, '🔍 أرسل الآن عنوان الـ IP الذي ترغب في التحقق منه.')

    # هنا ننتظر الرسالة التالية من المستخدم التي تحتوي على الـ IP
    @bot.message_handler(func=lambda m: True)
    def info(message):
        msg = message.text
        try:
            # جلب المعلومات من موقع ipinfo.io
            url = requests.get(f'https://ipinfo.io/{msg}/geo').json()
            ip = url.get('ip', 'غير متوفر')
            city = url.get('city', 'غير متوفر')
            region = url.get('region', 'غير متوفر')
            country = url.get('country', 'غير متوفر')
            loc = url.get('loc', 'غير متوفر')
            org = url.get('org', 'غير متوفر')
            timezone = url.get('timezone', 'غير متوفر')
            
            # إرسال المعلومات للمستخدم
            bot.send_message(message.chat.id, f'''
معلومات الـ IP ~ {ip} ⤵️

📍 المدينة: {city}
🌍 المنطقة: {region}
🏳️ رمز الدولة: {country}
🗺️ الموقع: {loc}
🏢 المنظمة: {org}
🕒 المنطقة الزمنية: {timezone}
            ''')
        
        except:
            bot.send_message(message.chat.id, '❌ تأكد من صحة عنوان الـ IP.')

# طباعة للتأكد من أن البوت يعمل
print('Bot is running...')
bot.infinity_polling()
