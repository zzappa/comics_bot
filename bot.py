import telebot

import links
import comic_downloader as codo

bot = telebot.TeleBot('insert_token_here')

keyboard = telebot.types.InlineKeyboardMarkup()
xkcd_random = telebot.types.InlineKeyboardButton(text='random xkcd', callback_data='xkcd_random')
xkcd_latest = telebot.types.InlineKeyboardButton(text='latest xkcd', callback_data='xkcd_latest')
goose_random = telebot.types.InlineKeyboardButton(text='random AbstruseGoose', callback_data='goose_random')
# goose_latest = telebot.types.InlineKeyboardButton(text='latest AbstruseGoose', callback_data='goose_latest')
poorlydrawnlines_random = telebot.types.InlineKeyboardButton(text='random poorly drawn lines', callback_data='poorlydrawnlines_random')
poorlydrawnlines_latest = telebot.types.InlineKeyboardButton(text='latest poorly drawn lines', callback_data='poorlydrawnlines_latest')
smbc_random = telebot.types.InlineKeyboardButton(text='random SMBC', callback_data='smbc_random')
smbc_latest = telebot.types.InlineKeyboardButton(text='latest SMBC', callback_data='smbc_latest')
keyboard.add(xkcd_random)
keyboard.add(xkcd_latest)
keyboard.add(goose_random)
# keyboard.add(goose_latest)
keyboard.add(poorlydrawnlines_random)
keyboard.add(poorlydrawnlines_latest)
keyboard.add(smbc_random)
keyboard.add(smbc_latest)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "xkcd_random":
        img, txt = codo.get_xkcd(links.xkcd_random)
        bot.send_photo(call.message.chat.id, img, txt)
    if call.data == "xkcd_latest":
        img, txt = codo.get_xkcd(links.xkcd_latest)
        bot.send_photo(call.message.chat.id, img, txt)
    if call.data == "goose_random":
        img = codo.get_goose(links.goose_random)
        bot.send_photo(call.message.chat.id, img)
    # there are no new abstrusegoose comics, so no need for 'latest' button
    # if call.data == "goose_latest":
    #     img = codo.get_goose(links.goose_latest, latest=True)
    #     bot.send_photo(call.message.chat.id, img)
    if call.data == "poorlydrawnlines_random":
        img = codo.get_poorlydrawnlines(links.poorlydrawnlines_random)
        if not img:
            bot.send_message(call.message.chat.id, "Smth went wrong, ahaha")
        else:
            bot.send_photo(call.message.chat.id, img)
    if call.data == "poorlydrawnlines_latest":
        img = codo.get_poorlydrawnlines(links.poorlydrawnlines_latest, latest=True)
        bot.send_photo(call.message.chat.id, img)
    if call.data == "smbc_random":
        img, txt = codo.get_smbc_from_archive(links.smbc_archive)
        if not img:
            bot.send_message(call.message.chat.id, "Smth went wrong, ahaha")
        else:
            bot.send_photo(call.message.chat.id, img, txt)
    if call.data == "smbc_latest":
        img, txt = codo.get_smbc(links.smbc_latest)
        bot.send_photo(call.message.chat.id, img, txt)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  if len(message.text) >= 1:
      bot.send_message(message.from_user.id, "Hello there! I'm ComicBot and I can show your some random comics."
                                             "\n'Choose a comic you want.'", reply_markup=keyboard)
  else:
      bot.send_message(message.from_user.id, "Please try again.")


bot.polling(none_stop=True, interval=0)
