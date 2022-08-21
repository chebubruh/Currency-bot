from telebot import *
from bs4 import BeautifulSoup
from requests import *
import config

bot = TeleBot(config.TOKEN)


# парсит инфу с БАНКИ.РУ
def parse_val():
    url = 'https://www.banki.ru/products/currency/cb/'
    r = get(url, headers=config.HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.find('tbody')
    data = data.text.replace('\n\n\n\n					', ';').replace('\n				\n', ' ').replace(
        '\n\n\n',
        ' ').replace(
        '\n\n					', ' ').replace(
        ' 					\n											',
        ' ').replace(
        '\n					\n											\n\n', ' ').replace(
        '\n											', ' ').replace(
        '\n					\n									\n', ' ').split(' ;')
    return data


# парсит инфу с investing.com
def parse_cval(x):
    url = f'https://ru.investing.com/crypto/{x}'
    r = get(url, headers=config.HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    price = soup.find('div', class_='top bold inlineblock').text.replace('\n', ' ').replace('\xa0', '').replace('  ',
                                                                                                                ' ').replace(
        '   ', ' ').split()
    return price


# строит основную клаву
@bot.message_handler(commands=['start'])
def start(message):
    general_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    v = types.KeyboardButton('Валюта 💰')
    c = types.KeyboardButton('Криптовалюта 💳')
    general_keyboard.add(v, c)
    bot.send_message(message.chat.id, 'Выбирай', reply_markup=general_keyboard)


# строит клаву с криптой или с обычной валютой
@bot.message_handler(func=lambda x: x.text == 'Валюта 💰' or x.text == 'Криптовалюта 💳')
def general(message):
    if message.text == 'Валюта 💰':
        vl_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        eur = types.KeyboardButton('🇪🇺 Евро')
        usd = types.KeyboardButton('🇺🇸 Доллар США')
        uah = types.KeyboardButton('🇺🇦 Гривна')
        try_ = types.KeyboardButton('🇹🇷 Лира')
        back = types.KeyboardButton('Назад')
        vl_keyboard.add(eur, usd, uah, try_, back)
        bot.send_message(message.chat.id, 'Выберите валюту', reply_markup=vl_keyboard)
    elif message.text == 'Криптовалюта 💳':
        cvl_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btc = types.KeyboardButton('Bitcoin')
        eth = types.KeyboardButton('Ethereum')
        doge = types.KeyboardButton('Dogecoin')
        usdt = types.KeyboardButton('Tether')
        back = types.KeyboardButton('Назад')
        cvl_keyboard.add(btc, eth, doge, usdt, back)
        bot.send_message(message.chat.id, 'Выберите криптовалюту', reply_markup=cvl_keyboard)


# отвечает курсом на крипту
@bot.message_handler(func=lambda
        x: x.text == 'Bitcoin' or x.text == 'Ethereum' or x.text == 'Dogecoin' or x.text == 'Tether' or x.text == 'Назад')
def cval(message):
    if message.text == 'Назад':
        start(message)
    elif message.text == 'Bitcoin':
        data = parse_cval('bitcoin')
        bot.send_message(message.chat.id, f'1 Bitcoin = <b>{data[1]} $</b>\n{data[3]}', parse_mode='HTML')
    elif message.text == 'Ethereum':
        data = parse_cval('ethereum')
        bot.send_message(message.chat.id, f'1 Ethereum = <b>{data[1]} $</b>\n{data[3]}', parse_mode='HTML')
    elif message.text == 'Dogecoin':
        data = parse_cval('dogecoin')
        bot.send_message(message.chat.id, f'1 Dogecoin = <b>{data[1]} $</b>\n{data[3]}', parse_mode='HTML')
    elif message.text == 'Tether':
        data = parse_cval('tether')
        bot.send_message(message.chat.id, f'1 Tether = <b>{data[1]} $</b>\n{data[3]}', parse_mode='HTML')


# отвечает курсом на валюту
@bot.message_handler(func=lambda
        x: x.text == '🇪🇺 Евро' or x.text == '🇺🇸 Доллар США' or x.text == '🇺🇦 Гривна' or x.text == '🇹🇷 Лира' or x.text == 'Назад')
def val(message):
    if message.text == 'Назад':
        start(message)
    elif message.text == '🇪🇺 Евро':
        data = parse_val()
        bot.send_message(message.chat.id, f'1 Евро = <b>{data[1][-15:-10]} ₽</b>\n{data[1][-7:]} (1 дн.)',
                         parse_mode="HTML")
    elif message.text == '🇺🇸 Доллар США':
        data = parse_val()
        bot.send_message(message.chat.id, f'1 Доллар США = <b>{data[0][-15:-10]} ₽</b>\n{data[0][-7:]} (1 дн.)',
                         parse_mode="HTML")
    elif message.text == '🇺🇦 Гривна':
        data = parse_val()
        bot.send_message(message.chat.id, f'1 Гривна = <b>{data[27][25:-10]} ₽</b>\n{data[27][-7:]} (1 дн.)',
                         parse_mode="HTML")
    elif message.text == '🇹🇷 Лира':
        data = parse_val()
        bot.send_message(message.chat.id, f'1 Лира = <b>{data[25][21:-10]} ₽</b>\n{data[25][-7:]} (1 дн.)',
                         parse_mode="HTML")


bot.polling(none_stop=True)
