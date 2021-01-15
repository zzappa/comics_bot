import telebot
import random

import links
import comic_downloader as codo
import apod

bot = telebot.TeleBot('insert-token-here')

error_msg = "Smth went wrong, ahaha. You can try again!"

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard_small = telebot.types.InlineKeyboardMarkup()
keyboard_start = telebot.types.InlineKeyboardMarkup()
keyboard_init = telebot.types.InlineKeyboardMarkup()
xkcd_random = telebot.types.InlineKeyboardButton(text='random xkcd', callback_data='xkcd_random')
xkcd_latest = telebot.types.InlineKeyboardButton(text='latest xkcd', callback_data='xkcd_latest')
goose_random = telebot.types.InlineKeyboardButton(text='random Abstruse Goose', callback_data='goose_random')
poorlydrawnlines_random = telebot.types.InlineKeyboardButton(text='random Poorly Drawn Lines',
                                                             callback_data='poorlydrawnlines_random')
poorlydrawnlines_latest = telebot.types.InlineKeyboardButton(text='latest Poorly Drawn Lines',
                                                             callback_data='poorlydrawnlines_latest')
smbc_random = telebot.types.InlineKeyboardButton(text='random SMBC', callback_data='smbc_random')
smbc_latest = telebot.types.InlineKeyboardButton(text='latest SMBC', callback_data='smbc_latest')
exo_random = telebot.types.InlineKeyboardButton(text='random Extra Ordinary', callback_data='exo_random')
exo_latest = telebot.types.InlineKeyboardButton(text='latest Extra Ordinary', callback_data='exo_latest')
tom_gauld_random = telebot.types.InlineKeyboardButton(text='random Tom Gauld', callback_data='tom_gauld_random')
tom_gauld_latest = telebot.types.InlineKeyboardButton(text='latest Tom Gauld', callback_data='tom_gauld_latest')
dilbert_random = telebot.types.InlineKeyboardButton(text='random Dilbert', callback_data='dilbert_random')
dilbert_latest = telebot.types.InlineKeyboardButton(text='latest Dilbert', callback_data='dilbert_latest')
phd_random = telebot.types.InlineKeyboardButton(text='random PhD comics', callback_data='phd_random')
phd_latest = telebot.types.InlineKeyboardButton(text='latest PhD comics', callback_data='phd_latest')
apod_random = telebot.types.InlineKeyboardButton(text='random APOD', callback_data='apod_random')
apod_latest = telebot.types.InlineKeyboardButton(text='latest APOD', callback_data='apod_latest')
again = telebot.types.InlineKeyboardButton(text='Yesss!', callback_data='again')
get_all_latest = telebot.types.InlineKeyboardButton(text='Get all latest comics!', callback_data='get_all_latest')
smth_random = telebot.types.InlineKeyboardButton(text='Surprise me!', callback_data='smth_random')
show_all = telebot.types.InlineKeyboardButton(text='Nah, show me all options.', callback_data='show_all')
start = telebot.types.InlineKeyboardButton(text='Start!', callback_data='start')
keyboard.row(xkcd_random, xkcd_latest)
keyboard.add(goose_random)
keyboard.row(poorlydrawnlines_random, poorlydrawnlines_latest)
keyboard.row(smbc_random, smbc_latest)
keyboard.row(exo_random, exo_latest)
keyboard.row(tom_gauld_random, tom_gauld_latest)
keyboard.row(dilbert_random, dilbert_latest)
keyboard.row(phd_random, phd_latest)
keyboard.row(apod_random, apod_latest)
keyboard.add(smth_random)
keyboard_small.add(again)
keyboard_start.add(get_all_latest)
keyboard_start.add(smth_random)
keyboard_start.add(show_all)
keyboard_init.add(start)


def return_comic(call, get_comic, link, latest=False):
    if not latest:
        img, txt = get_comic(link)
    else:
        img, txt = get_comic(link, latest)
    if get_comic in (apod.get_apod, apod.get_apod_random):
        bot.send_message(call.message.chat.id, txt)
    elif not img:
        bot.send_message(call.message.chat.id, error_msg, reply_markup=keyboard_small)
    else:
        bot.send_photo(call.message.chat.id, img, txt)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    def _again():
        bot.send_message(call.message.chat.id, "Again?", reply_markup=keyboard_small)

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
        return_comic(call, codo.get_poorlydrawnlines, links.poorlydrawnlines_random)
        _again()
    if call.data == "poorlydrawnlines_latest":
        return_comic(call, codo.get_poorlydrawnlines, links.poorlydrawnlines_latest, latest=True)
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
    if call.data in ("again", "show_all"):
        bot.send_message(call.message.chat.id, 'Choose wisely!', reply_markup=keyboard)
    if call.data == "get_all_latest":
        return_comic(call, codo.get_xkcd, links.xkcd_latest)
        return_comic(call, codo.get_poorlydrawnlines, links.poorlydrawnlines_latest, latest=True)
        return_comic(call, codo.get_smbc, links.smbc_latest)
        return_comic(call, codo.get_exo, links.exo_latest)
        return_comic(call, codo.get_tom_gauld, links.tom_gauld_latest)
        bot.send_message(call.message.chat.id, 'Here you go! Want more?', reply_markup=keyboard_small)
    if call.data == "smth_random":
        random_list = [(codo.get_xkcd, links.xkcd_random),
                       (codo.get_goose, links.goose_random),
                       (codo.get_poorlydrawnlines, links.poorlydrawnlines_random),
                       (codo.get_smbc_from_archive, links.smbc_archive),
                       (codo.get_exo_archive, links.exo_archive),
                       (codo.get_tom_gauld, links.tom_gauld_random),
                       (codo.get_dilbert, links.dilbert),
                       (codo.get_phd_random, links.phd_archive),
                       (apod.get_apod_random, links.apod_archive)]
        func, link = random.choice(random_list)
        return_comic(call, func, link)
        _again()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if len(message.text) >= 1 and message.text.lower() != 'start':
        bot.send_message(message.chat.id,
                         "Hello there! I'm TheComicBot and I can show your some comics."
                         "\nChoose a comic you want.",
                         reply_markup=keyboard)
    elif message.text.lower() == 'start':
        bot.send_message(message.chat.id,
                         "Hello there! I'm TheComicBot! What do you want?",
                         reply_markup=keyboard_start)
    else:
        bot.send_message(message.from_user.id, "Please try again.")


bot.polling(none_stop=True, interval=0)
