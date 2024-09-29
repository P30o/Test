from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# قائمة لتخزين بيانات اللاعبين
players = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحباً! استخدم /add لإضافة لاعب.')

def add_player(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text('الرجاء إدخال اسم اللاعب والسعر.')
        return

    name = context.args[0]
    price = int(context.args[1])
    bullets = 50
    total_price = price

    if name in players:
        players[name]['bullets'] += bullets
        players[name]['total_price'] += 5000  # زيادة 5000 دينار لكل 50 طلقة إضافية
    else:
        players[name] = {'price': price, 'bullets': bullets, 'total_price': total_price}

    update.message.reply_text(f"تم إضافة اللاعب: {name} بسعر: {total_price} دينار و {bullets} طلقة.")

def get_players(update: Update, context: CallbackContext) -> None:
    if not players:
        update.message.reply_text('لا يوجد لاعبين مضافين.')
        return

    message = 'قائمة اللاعبين:\n'
    for name, details in players.items():
        message += f"الاسم: {name}, السعر: {details['total_price']} دينار، الطلقات: {details['bullets']}\n"

    update.message.reply_text(message)

def main() -> None:
    # ضع هنا الـ TOKEN الخاص بك
    updater = Updater("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("add", add_player))
    updater.dispatcher.add_handler(CommandHandler("players", get_players))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
