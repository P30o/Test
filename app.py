from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import logging
import pickle

# إعدادات تسجيل الدخول
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تحميل أو إنشاء قائمة اللاعبين
try:
    with open('players.pkl', 'rb') as f:
        players = pickle.load(f)
except FileNotFoundError:
    players = []

# تعريف نقاط المحادثة
PLAYER_NAME, TEAM_NAME = range(2)

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('أهلاً بك في بوت تسجيل اللاعبين! استخدم الأمر /add لتسجيل لاعب جديد أو /list لعرض اللاعبين.')

def add_player(update: Update, _: CallbackContext) -> int:
    update.message.reply_text('أدخل اسم اللاعب:')
    return PLAYER_NAME

def player_name(update: Update, context: CallbackContext) -> int:
    context.user_data['player_name'] = update.message.text
    update.message.reply_text('أدخل اسم الفريق:')
    return TEAM_NAME

def team_name(update: Update, context: CallbackContext) -> int:
    context.user_data['team_name'] = update.message.text
    player = {
        'playerName': context.user_data['player_name'],
        'teamName': context.user_data['team_name'],
        'bullets': 50,
        'smokes': 0
    }
    players.append(player)
    with open('players.pkl', 'wb') as f:
        pickle.dump(players, f)
    update.message.reply_text(f"تم إضافة اللاعب {player['playerName']} في الفريق {player['teamName']}.")
    return ConversationHandler.END

def list_players(update: Update, _: CallbackContext) -> None:
    if not players:
        update.message.reply_text('لا يوجد لاعبين مسجلين.')
    else:
        message = "قائمة اللاعبين:\n"
        total_price = 0
        for player in players:
            price = calculate_price(player['bullets'], player['smokes'])
            total_price += price
            message += f"\nاسم الفريق: {player['teamName']}, اسم اللاعب: {player['playerName']}, الطلقات: {player['bullets']}, اسموك: {player['smokes']}, السعر: {price} دينار عراقي"
        message += f"\n\nالسعر الإجمالي لجميع اللاعبين: {total_price} دينار عراقي"
        update.message.reply_text(message)

def calculate_price(bullets: int, smokes: int) -> int:
    initial_cost = 7000
    extra_bullets_cost = max((bullets - 50) / 50 * 5000, 0)
    smokes_cost = smokes * 2000
    return int(initial_cost + extra_bullets_cost + smokes_cost)

def main() -> None:
    # ضع هنا توكن البوت الخاص بك
    updater = Updater("7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY")

    dispatcher = updater.dispatcher

    # أوامر البوت
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list", list_players))

    # معالجة المحادثة لللاعبين
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_player)],
        states={
            PLAYER_NAME: [MessageHandler(Filters.text & ~Filters.command, player_name)],
            TEAM_NAME: [MessageHandler(Filters.text & ~Filters.command, team_name)],
        },
        fallbacks=[]
    )
    dispatcher.add_handler(conv_handler)

    # تشغيل البوت
    updater.start_polling()

    # إيقاف البوت عند الضغط على Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
