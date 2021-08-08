import logging
import sys
import validators

from queue import Queue
from threading import Thread
from waitress import serve
from flask import Flask, request

from telegram import Bot, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import Dispatcher, MessageHandler, Filters

from settings import TOKEN
from ..tracker.tracker import Tracker

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('server')

bot = Bot(TOKEN)
update_queue = Queue()
dispatcher = Dispatcher(bot, update_queue)
thread = Thread(target=dispatcher.start, name='dispatcher')

app = Flask('echo')

users_to_track = {}


def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user

    users_to_track[user] = Tracker()

    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Бот позволяет отслеживать изменения цен и описания авито объявлений. ')


def add_ad(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    url = update.message.text.split(' ')[1]

    if validators.url(url):
        users_to_track[user].add(url)
        update.message.reply_text('Добавлено для отслеживания.')
    else:
        update.message.reply_text('Не корректная ссылка.')


def check_updates(update: Update, _: CallbackContext) -> None:
    user = update.effective_user

    ad_updates = users_to_track[user].update()

    if ad_updates:
        update.message.reply_text(ad_updates)
    else:
        update.message.reply_text('Нет изменений')


def delete_ad(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    url = update.message.text.split(' ')[1]

    if validators.url(url):
        users_to_track[user].delete(url)
        update.message.reply_text('Объявление теперь не отслеживается.')
    else:
        update.message.reply_text('Не корректная ссылка.')


def wrong_data(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Sorry, we work only with photo or text')


@app.route(f'/{TOKEN}', methods=['POST'])
def echo():
    logger.info(request.get_json())
    update = Update.de_json(request.json, bot)
    update_queue.put(update)
    return {'ok': True}


def set_handlers():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler("add_ad", add_ad))
    dispatcher.add_handler(CommandHandler("check_updates", check_updates))
    dispatcher.add_handler(CommandHandler("delete_ad", delete_ad))

    dispatcher.add_handler(MessageHandler(~Filters.text, wrong_data))


if __name__ == '__main__':
    set_handlers()

    thread.start()

    bot.setWebhook(f'{sys.argv[1]}/{TOKEN}')
    serve(app, host='0.0.0.0', port='2781')
