import telebot
from config import TOKEN, exchanges
from extensions import APIException, Converter

# https://api.exchangeratesapi.io/v1/latest?access_key=bc5d1fd654f0301b98231df92fed3bed&format=1
# https://www.cbr-xml-daily.ru/latest.js

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты> \n Увидеть список всех доступных валют /values'

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        base, quote, amount = values
        answer = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        bot.reply_to(message, answer)

bot.polling()