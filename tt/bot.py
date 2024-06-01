from config import token
import telebot
import os

API_TOKEN = '<api_token>'

bot = telebot.TeleBot(token)

class Car:
    def __init__(self, color, brand):
        self.color = color
        self.brand = brand
    
    def info(self):
        return f"Это машина марки {self.brand} цвета {self.color}."

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я Эхобот.
Я здесь, чтобы ответить вам добрыми словами. Просто скажите что-нибудь приятное, и я отвечу вам тем же!\
""")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "Это бот для эхо-ответов. Просто напишите что-нибудь, и я повторю это!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("saved_photo.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.reply_to(message, "Спасибо за фото! Я его сохранил.")

@bot.message_handler(commands=['car'])
def handle_car(message):
    arguments = message.text.split()[1:]  
    if len(arguments) != 2:
        bot.reply_to(message, "Неверное количество аргументов. Используйте команду /car цвет марка.")
    else:
        color, brand = arguments
        car = Car(color, brand)
        bot.reply_to(message, car.info())

bot.infinity_polling()
