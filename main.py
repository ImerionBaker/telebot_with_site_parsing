import telebot
from telebot import types

import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot("TOKEN")
URL = 'http://www.kantorredar.pl/index.php/kursy-walut/#detal'

tmp = 0
tmp_kod = ''
user_much = ''
euro_buy = 0
euro_sell = 0
dollar_buy = 0
dollar_sell = 0
end_value = 0
uah_buy = 0
uah_sell = 0
byn_buy = 0
byn_sell = 0




@bot.message_handler(commands=['start'])
def star(message):
    bot.send_message(message.from_user.id, 'Hello! This is exchange program. There is a list of command. Choose one!'
                                           '\n/exchange - to see how many you get'
                                           '\n/courses - to see actual courses')



@bot.message_handler(commands=['exchange'])
def send_welcome(message):
    opt = 'Choose option(write number in the chat)\n1. Excnange EUR to PLN\n2. Excnange PLN to EUR\n3. Excnange USD to PLN\n4. Excnange PLN to USD\n5. Excnange UAH to PLN\n6. Excnange PLN to UAH\n7. Excnange BYN to PLN\n8. Excnange PLN to BYN'
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='1', callback_data='1')
    keyboard.add(key_1)

    key_2 = types.InlineKeyboardButton(text='2', callback_data='2')
    keyboard.add(key_2)

    key_3 = types.InlineKeyboardButton(text='3', callback_data='3')
    keyboard.add(key_3)

    key_4 = types.InlineKeyboardButton(text='4', callback_data='4')
    keyboard.add(key_4)

    key_5 = types.InlineKeyboardButton(text='5', callback_data='5')
    keyboard.add(key_5)

    key_6 = types.InlineKeyboardButton(text='6', callback_data='6')
    keyboard.add(key_6)

    key_7 = types.InlineKeyboardButton(text='7', callback_data='7')
    keyboard.add(key_7)

    key_8 = types.InlineKeyboardButton(text='8', callback_data='8')
    keyboard.add(key_8)

    bot.send_message(message.from_user.id, text=opt, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global tmp
    global tmp_kod

    if call.data == "1":
        tmp = 1
        tmp_kod = 'EUR'

    elif call.data == "2":
        tmp = 2
        tmp_kod = 'PLN'

    elif call.data == "3":
        tmp = 3
        tmp_kod = 'USD'
    elif call.data == "4":
        tmp = 4
        tmp_kod = 'PLN'
    elif call.data == "5":
        tmp = 5
        tmp_kod = 'UAH'
    elif call.data == "6":
        tmp = 6
        tmp_kod = 'PLN'
    elif call.data == "7":
        tmp = 7
        tmp_kod = 'BYN'
    elif call.data == "8":
        tmp = 8
        tmp_kod = 'PLN'
    bot.send_message(call.message.chat.id, 'Enter how much ' + tmp_kod + ' you want to exchange')
    bot.register_next_step_handler(call.message, result)


@bot.message_handler(commands=['courses'])
def sen(message):
    parse()
    bot.send_message(message.from_user.id,'Courses: \nUSD\nBuy: '+str(dollar_buy) + '\nSell: ' + str(dollar_sell)+
                     '\nEUR\nBuy: ' + str(euro_buy) + '\nSell: ' + str(euro_sell) + '\nUAH\nBuy: '+str(uah_buy) + '\nSell: ' + str(uah_sell) +
                     '\nBYN\nBuy: '+str(byn_buy) + '\nSell: ' + str(byn_sell) +'\nWrite /start if you want to see something else')





def get_html(url, params=None):
    r = requests.get(url, params=params)
    return  r

def get_content(html):
    global tmp_kod
    global user_much
    global tmp
    global euro_buy
    global euro_sell
    global dollar_sell
    global dollar_buy
    global end_value
    global uah_sell
    global uah_buy
    global byn_sell
    global byn_buy
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('tr', id='igsv-1-1ommxVLyqbi7D-AfOrgK5NcpWNkaoQjXQPJz9T_vpH0Y-row-2')
    items_eur = soup.find_all('tr', id='igsv-1-1ommxVLyqbi7D-AfOrgK5NcpWNkaoQjXQPJz9T_vpH0Y-row-3')
    items_uah = soup.find_all('tr', id='igsv-1-1ommxVLyqbi7D-AfOrgK5NcpWNkaoQjXQPJz9T_vpH0Y-row-183')
    items_byn = soup.find_all('tr', id='igsv-1-1ommxVLyqbi7D-AfOrgK5NcpWNkaoQjXQPJz9T_vpH0Y-row-29')

    for item in items_eur:
        euro_buy = float(str.replace(item.find('td', class_='col-5').get_text(), ',', '.'))
        euro_sell = float(str.replace(item.find('td', class_='col-6').get_text(), ',', '.'))

    for item in items:
        dollar_buy = float(str.replace(item.find('td', class_='col-5').get_text(), ',', '.'))
        dollar_sell = float(str.replace(item.find('td', class_='col-6').get_text(), ',', '.'))

    for item in items_uah:
        uah_buy = float(str.replace(item.find('td', class_='col-5').get_text(), ',', '.'))
        uah_sell = float(str.replace(item.find('td', class_='col-6').get_text(), ',', '.'))

    for item in items_byn:
        byn_buy = float(str.replace(item.find('td', class_='col-5').get_text(), ',', '.'))
        byn_sell = float(str.replace(item.find('td', class_='col-6').get_text(), ',', '.'))

    end_value = float()

    if tmp == 1:
        end_value = round(float(user_much) * float(euro_buy),2)
        tmp_kod = 'PLN'
    elif tmp == 2:
        end_value = round(float(user_much) / float(euro_sell),2)
        tmp_kod = 'EUR'
    elif tmp == 3:
        end_value = round(float(user_much) * float(dollar_buy),2)
        tmp_kod = 'PLN'
    elif tmp == 4:
        end_value = round(float(user_much) / float(dollar_sell),2)
        tmp_kod = 'USD'
    elif tmp == 5:
        end_value = round(float(user_much) * float(uah_buy),2)
        tmp_kod = 'PLN'
    elif tmp == 6:
        end_value = round(float(user_much) / float(uah_sell),2)
        tmp_kod = 'UAH'
    elif tmp == 7:
        end_value = round(float(user_much) * float(byn_buy),2)
        tmp_kod = 'PLN'
    elif tmp == 8:
        end_value = round(float(user_much) / float(byn_sell),2)
        tmp_kod = 'BYN'



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')



def result(message):
    global end_value
    global tmp_kod
    global user_much
    try:
        user_much = float(message.text)
        parse()
        bot.send_message(message.from_user.id, 'You get: ' + str(end_value) + ' ' + tmp_kod + '\nWrite /start if you want to see something else')
    except Exception:
        bot.send_message(message.from_user.id, 'Write a number!')
        bot.register_next_step_handler(message,result)

bot.polling()
