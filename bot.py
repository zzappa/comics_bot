import random
from datetime import datetime
from dateutil import parser
import feedparser
import logging
import schedule
import time
from threading import Thread
import pytz

import links
import comic_downloader as codo
import apod
from bot_init import bot, keyboard, keyboard_start, keyboard_small, keyboard_sub

DEBUG = True
chat_id = ''
subscribe = False
error_msg = "Smth went wrong, ahaha. You can try again!"


def return_comic(call, get_comic, link, latest=False):
    if not latest:
        img, txt = get_comic(link)
    else:
        img, txt = get_comic(link, latest)
    if 'apod' in link:
        bot.send_message(call.message.chat.id, txt, parse_mode='Markdown')
    elif not img:
        bot.send_message(call.message.chat.id, error_msg, reply_markup=keyboard_small)
    else:
        bot.send_photo(call.message.chat.id, img, txt, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    def _again():
        bot.send_message(call.message.chat.id, "Again?", reply_markup=keyboard_small)

    global chat_id, subscribe
    chat_id = call.message.chat.id
    if call.data == "xkcd_random":
        return_comic(call, codo.get_xkcd, links.xkcd_random)
        _again()
    if call.data == "xkcd_latest":
        return_comic(call, codo.get_xkcd, links.xkcd_latest)
        _again()
    if call.data == "goose_random":
        return_comic(call, codo.get_goose, links.goose_random)
        _again()
    if call.data == "poorlydrawnlines_random":
        return_comic(call, codo.get_poorlydrawnlines_archive, links.poorlydrawnlines_random)
        _again()
    if call.data == "poorlydrawnlines_latest":
        return_comic(call, codo.get_poorlydrawnlines, links.poorlydrawnlines_latest)
        _again()
    if call.data == "smbc_random":
        return_comic(call, codo.get_smbc_from_archive, links.smbc_archive)
        _again()
    if call.data == "smbc_latest":
        return_comic(call, codo.get_smbc, links.smbc_latest)
        _again()
    if call.data == "exo_random":
        return_comic(call, codo.get_exo_archive, links.exo_archive)
        _again()
    if call.data == "exo_latest":
        return_comic(call, codo.get_exo, links.exo_latest)
        _again()
    if call.data == "tom_gauld_random":
        return_comic(call, codo.get_tom_gauld, links.tom_gauld_random)
        _again()
    if call.data == "tom_gauld_latest":
        return_comic(call, codo.get_tom_gauld, links.tom_gauld_latest)
        _again()
    if call.data == "dilbert_latest":
        return_comic(call, codo.get_dilbert, links.dilbert, latest=True)
        _again()
    if call.data == "dilbert_random":
        return_comic(call, codo.get_dilbert, links.dilbert)
        _again()
    if call.data == "phd_random":
        return_comic(call, codo.get_phd_random, links.phd_archive)
        _again()
    if call.data == "phd_latest":
        return_comic(call, codo.get_phd, links.phd_latest)
        _again()
    if call.data == "apod_latest":
        return_comic(call, apod.get_apod, links.apod_latest)
        _again()
    if call.data == "apod_random":
        return_comic(call, apod.get_apod_random, links.apod_archive)
        _again()
    if call.data == "new_yorker":
        res = codo.get_new_yorker_rss(links.new_yorker_daily_rss)
        for item in res:
            for i, txt in item:
                if not i:
                    bot.send_message(call.message.chat.id, error_msg, reply_markup=keyboard_small,
                                     parse_mode='Markdown')
                else:
                    bot.send_photo(call.message.chat.id, i, txt)
        _again()
    if call.data in ("again", "show_all"):
        bot.send_message(call.message.chat.id, 'Choose wisely!', reply_markup=keyboard)
    if call.data == "get_all_latest":
        return_comic(call, codo.get_xkcd, links.xkcd_latest)
        return_comic(call, codo.get_poorlydrawnlines, links.poorlydrawnlines_latest)
        return_comic(call, codo.get_smbc, links.smbc_latest)
        return_comic(call, codo.get_exo, links.exo_latest)
        return_comic(call, codo.get_tom_gauld, links.tom_gauld_latest)
        return_comic(call, codo.get_dilbert, links.dilbert)
        return_comic(call, codo.get_phd, links.phd_latest)
        return_comic(call, apod.get_apod, links.apod_latest)
        bot.send_message(call.message.chat.id, 'Here you go! Want more?', reply_markup=keyboard_small)
    if call.data == "smth_random":
        random_list = [(codo.get_xkcd, links.xkcd_random),
                       (codo.get_goose, links.goose_random),
                       (codo.get_poorlydrawnlines_archive, links.poorlydrawnlines_random),
                       (codo.get_smbc_from_archive, links.smbc_archive),
                       (codo.get_exo_archive, links.exo_archive),
                       (codo.get_tom_gauld, links.tom_gauld_random),
                       (codo.get_dilbert, links.dilbert),
                       (codo.get_phd_random, links.phd_archive),
                       (apod.get_apod_random, links.apod_archive)]
        func, link = random.choice(random_list)
        return_comic(call, func, link)
        _again()
    if call.data == "subscribe":
        logging.warning("chat id " + str(chat_id))
        chat_id = call.message.chat.id
        subscribe = True
        logging.warning("You've got subscribed")
        bot.send_message(call.message.chat.id, "You've got subscribed :)")
    if call.data == "unsubscribe":
        subscribe = False
        logging.warning("You've got unsubscribed")
        bot.send_message(call.message.chat.id, "You've got unsubscribed :(")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if len(message.text) >= 1 and message.text.lower() not in ('start', 'subscribe', 'unsubscribe'):
        bot.send_message(message.chat.id,
                         "Hello there! I'm TheComicBot and I can show your some comics."
                         "\nChoose a comic you want.",
                         reply_markup=keyboard)
    elif message.text.lower() in ('start'):
        bot.send_message(message.chat.id,
                         "Hello there! I'm TheComicBot! What do you want?",
                         reply_markup=keyboard_start)
    elif message.text.lower() in ('subscribe', 'unsubscribe'):
        bot.send_message(message.chat.id, 'Do you want to change subscription?',
                         reply_markup=keyboard_sub)
    else:
        bot.send_message(message.from_user.id, "Please try again.")


def rss_monitor():
    """Checks rss, returns new images if their date is today."""
    utc = pytz.UTC
    rss_list = (
        (codo.get_xkcd, links.xkcd_rss),
        (codo.get_smbc, links.smbc_rss),
        (codo.get_poorlydrawnlines, links.poorlydrawnlines_rss),
        (codo.get_exo, links.exo_rss),
        (codo.get_tom_gauld, links.tom_gauld_rss),
        (codo.get_dilbert, links.dilbert),
        (codo.get_phd, links.phd_rss),
        (apod.get_apod, links.apod_latest),
    )

    def _check(func, rss):
        logging.warning(str(subscribe))
        if subscribe:
            try:
                rss_feed = feedparser.parse(rss)
                logging.warning('checking rss')
                parsed_date = parser.parse(rss_feed.entries[0].published)
                today = utc.localize(datetime.today()).day, utc.localize(datetime.today()).month
                yesterday = utc.localize(datetime.today()).day - 1, utc.localize(datetime.today()).month
                if (parsed_date.day, parsed_date.month) in (today, yesterday) or parsed_date.day > today[0]:
                    url = rss_feed.entries[0].link
                else:
                    url = None
            except Exception:
                url = rss
            if url:
                if 'dilbert' in rss:
                    i, txt = func(rss, latest=True)
                else:
                    i, txt = func(url)
                if 'apod' in rss:
                    bot.send_message(chat_id, txt, parse_mode='Markdown')
                else:
                    bot.send_photo(chat_id, i, txt, parse_mode='Markdown')

    for func, rss in rss_list:
        _check(func, rss)


def do_schedule():
    if DEBUG:
        schedule.every(5).seconds.do(rss_monitor)
    else:
        schedule.every().day.at("13:37").do(rss_monitor)
    while True:
        schedule.run_pending()
        time.sleep(1)


def main_loop():
    thread = Thread(target=do_schedule)
    thread.start()

    bot.polling(True)


if __name__ == '__main__':
    main_loop()
