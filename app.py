import requests
import telebot
from telebot import types

# ضع توكن البوت الخاص بك هنا
bot_token = "7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY"  # احذف كلمة توكنك وأضف التوكن الخاص بك
bot = telebot.TeleBot(bot_token)

# API الخاص بموقع Numverify (تحتاج إلى التسجيل للحصول على مفتاح API)
api_key = "31f7f11224bb0c7d6439de6f2f768533"  # ضع مفتاح API الخاص بك هنا

# زر Inline لإجراء الفحص
btn1 = types.InlineKeyboardButton(text='🔍 تحقق من رقم الهاتف', callback_data='check_phone')

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
في بوت معلومات رقم الهاتف.
أرسل رقم الهاتف مع رمز الدولة (+964...).
**''', parse_mode='Markdown', reply_markup=brok)

@bot.callback_query_handler(func=lambda call: call.data == 'check_phone')
def phone(call):
    bot.send_message(call.message.chat.id, '🔍 أرسل الآن رقم الهاتف الذي ترغب في التحقق منه (مع رمز الدولة).')

    # هنا ننتظر الرسالة التالية من المستخدم التي تحتوي على رقم الهاتف
    @bot.message_handler(func=lambda m: True)
    def phone_info(message):
        phone_number = message.text
        try:
            # جلب المعلومات من Numverify API
            url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"
            response = requests.get(url).json()

            if response['valid']:
                number = response.get('number', 'غير متوفر')
                country_name = response.get('country_name', 'غير متوفر')
                location = response.get('location', 'غير متوفر')
                carrier = response.get('carrier', 'غير متوفر')
                line_type = response.get('line_type', 'غير متوفر')
                
                # إرسال المعلومات للمستخدم
                bot.send_message(message.chat.id, f'''
معلومات رقم الهاتف ~ {number} ⤵️

🏳️ الدولة: {country_name}
📍 الموقع: {location}
📡 مزود الخدمة: {carrier}
📞 نوع الخط: {line_type}
                ''')
            else:
                bot.send_message(message.chat.id, '❌ الرقم غير صالح. تأكد من إدخال الرقم بشكل صحيح.')
        
        except:
            bot.send_message(message.chat.id, '❌ حدث خطأ أثناء جلب المعلومات. حاول مرة أخرى لاحقاً.')

# طباعة للتأكد من أن البوت يعمل
print('Bot is running...')
bot.infinity_polling()
