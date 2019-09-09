#============const===========
api_key = '<bot_token>'
purse = 'https://bitly.su/YeNo'


#=========import
import glob
import telebot
import sqlite3
import random
from highlighter import make_image, get_languages
#================functions
def err(Lists):
	Lists = Lists.replace('"', "'")
	return Lists


def get_random_bg():
    return random.choice(glob.glob("templates/pycharm/*.jpg"))

def db_log(message):
	print('Sent to @' + str(message.chat.username) + '; id = ' + str(message.chat.id) + '; text = ' + str(message.text))
	conn = sqlite3.connect("data_baz.sqlite")
	cursor = conn.cursor()
	cursor.execute('insert into messages(id, text, name) VALUES ( "' + str(message.chat.id) + '", "' + err(str(message.text)) + '", "@' + err(str(message.chat.username)) + '");')
	conn.commit()
	conn.close()



bot = telebot.TeleBot(api_key)

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Hello @' + str(message.chat.username) +'!!!\nI can make a photo with a code from your code.\nWrite /help to find out all the commands\n\nLicense: AGPL-3.0 https://github.com/drogi17/codephoto_bot')
	db_log(message)

@bot.message_handler(commands=['help'])
def start_message(message):
	db_log(message)
	bot.send_message(message.chat.id, '''
Commands:
   /info
   /start
   /help
   /donate
''')

@bot.message_handler(commands=['donate'])
def start_message(message):
	db_log(message)
	bot.send_message(message.chat.id, purse)

@bot.message_handler(commands=['info'])
def start_message(message):
	db_log(message)
	bot.send_message(message.chat.id, '''
Adapted Version: t.me/codephoto_bot
Adapted link to the project: https://github.com/drogi17/codephoto_bot
Adapted by: @Drogi17
Original project: http://codephoto.ru/
Link to the project: https://github.com/Tishka17/codephoto
Original developer: @Tishka17
''')



@bot.message_handler(content_types=['text'])
def get_code(message):
	make_image(str(message.text), "upload/123123.jpg", "", background=get_random_bg())
	photo = open('upload/123123.jpg', 'rb')
	bot.send_photo(message.chat.id, photo)
	db_log(message)
	




bot.polling()