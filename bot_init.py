import telebot

token = 'insert-token-here'
bot = telebot.TeleBot(token)

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard_small = telebot.types.InlineKeyboardMarkup()
keyboard_start = telebot.types.InlineKeyboardMarkup()
keyboard_sub = telebot.types.InlineKeyboardMarkup()
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
pbf_random = telebot.types.InlineKeyboardButton(text='random Perry Bible Fellowship', callback_data='pbf_random')
pbf_latest = telebot.types.InlineKeyboardButton(text='latest Perry Bible Fellowship', callback_data='pbf_latest')
new_yorker = telebot.types.InlineKeyboardButton(text='The New Yorker Daily Cartoon', callback_data='new_yorker')
calvinandhobbes = telebot.types.InlineKeyboardButton(text='random Calvin and Hobbes', callback_data='calvinandhobbes')
garfield = telebot.types.InlineKeyboardButton(text='random Garfield', callback_data='garfield')
pearlsbeforeswine = telebot.types.InlineKeyboardButton(text='random Pearls Before Swine', callback_data='pearlsbeforeswine')
again = telebot.types.InlineKeyboardButton(text='Yesss!', callback_data='again')
get_all_latest = telebot.types.InlineKeyboardButton(text='Get all latest comics!', callback_data='get_all_latest')
smth_random = telebot.types.InlineKeyboardButton(text='Surprise me!', callback_data='smth_random')
show_all = telebot.types.InlineKeyboardButton(text='Nah, show me all options.', callback_data='show_all')
subscribe = telebot.types.InlineKeyboardButton(text='Subscribe!', callback_data='subscribe')
unsubscribe = telebot.types.InlineKeyboardButton(text='Unsubscribe?', callback_data='unsubscribe')
keyboard.row(xkcd_random, xkcd_latest)
keyboard.add(goose_random)
keyboard.row(poorlydrawnlines_random, poorlydrawnlines_latest)
keyboard.row(smbc_random, smbc_latest)
keyboard.row(exo_random, exo_latest)
keyboard.row(tom_gauld_random, tom_gauld_latest)
keyboard.row(dilbert_random, dilbert_latest)
keyboard.row(phd_random, phd_latest)
keyboard.row(apod_random, apod_latest)
keyboard.add(new_yorker)
keyboard.row(pbf_random, pbf_latest)
keyboard.add(calvinandhobbes)
keyboard.add(garfield)
keyboard.add(pearlsbeforeswine)
keyboard.add(smth_random)
keyboard_small.add(again)
keyboard_start.add(get_all_latest)
keyboard_start.add(smth_random)
keyboard_start.add(show_all)
keyboard_sub.add(subscribe)
keyboard_sub.add(unsubscribe)
