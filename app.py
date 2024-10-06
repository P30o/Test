import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
import string

# تفعيل التسجيل (logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# دالة لتوليد رابط فريد للمستخدم
def generate_unique_link(user_id):
    unique_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return f"https://safepichub.netlify.app?user={user_id}&code={unique_code}"

# دالة تعالج الأمر /start
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_agent = update.message.from_user.username  # يمكنك تغيير ذلك إلى ما تراه مناسبًا

    # توليد الرابط الفريد
    unique_link = generate_unique_link(user_id)

    # إرسال الرسالة للمستخدم
    message = f"User Agent: {user_agent} | Unique Link: {unique_link}"
    update.message.reply_text(message)

def main():
    # استبدل TOKEN الخاص بك هنا
    updater = Updater("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

    dispatcher = updater.dispatcher

    # إضافة معالج للأمر /start
    dispatcher.add_handler(CommandHandler("start", start))

    # بدء البوت
    updater.start_polling()

    # البقاء في حالة تشغيل حتى يتم إيقافه
    updater.idle()

if __name__ == '__main__':
    main()
