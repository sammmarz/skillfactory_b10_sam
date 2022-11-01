"' Основной файл бота конвертора валют '"
import telebot
from config import TOKEN, currencies
from extensions import APIException, Convert

bot = telebot.TeleBot(TOKEN)

# обработчик команд start and help
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = "Для начала работы введите команду в следующем формате: \n<имя валюты>\
<в какую перевести>\
<количество>\n Посмотреть доступные валюты: /values"
    bot.reply_to(message, text)

# обработчик команды values(список доступных валют)
@bot.message_handler(commands=['values'])
def values(message):
    text = 'Список доступных для конвертации валют:'
    for key in currencies.keys():
        text ='\n'.join((text, key))
    bot.reply_to(message, text)

# функция-обработчик данных для конвертации
@bot.message_handler(content_types=['text'])
def convert(message):

    try:
        values = message.text.split()
        if len(values) > 3:
            raise APIException('Слишком много параметров')
        quote, base, amount = values

        total_base = Convert.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

# запуск бота
bot.polling(none_stop=True)

