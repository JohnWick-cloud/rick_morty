from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from main import ad_link

enable = KeyboardButton("Вкл")
disable = KeyboardButton('Выкл')
sub_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(enable,disable)


# sezon1 = KeyboardButton(1)
# sezon2 = KeyboardButton(2)
# sezon3 = KeyboardButton(3)
# sezon4 = KeyboardButton(4)
# sezon_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(sezon1, sezon2, sezon3, sezon4)

def btn_creator(count):
    dictionary = [a for a in range(1, count+1)]
    btn = []
    for i in dictionary:
        btn.append(KeyboardButton(f'{i} серия'))
    btn.append(KeyboardButton("Назад"))
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*btn)
    return menu

link = ad_link.split('@')
sub_link = InlineKeyboardButton("КАНАЛ",url=f'https://t.me/{link[1]}')
sub_btn = InlineKeyboardButton('ПРОВЕРИТЬ ПОДПИСКУ', callback_data='done')
ad_menu = InlineKeyboardMarkup(row_width=1).add(sub_link, sub_btn)

def sezon_creation(sezons):
    btn = []
    for sezon in sezons:
        btn.append(KeyboardButton(sezon))
    btn.append(KeyboardButton("Назад"))
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*btn)
    return menu

link_sez = ad_link.split('@')
sub_link_sez = InlineKeyboardButton("КАНАЛ",url=f'https://t.me/{link_sez[1]}')
sub_btn_sez = InlineKeyboardButton('ПРОВЕРИТЬ ПОДПИСКУ', callback_data='done_sez')
ad_menu_sez = InlineKeyboardMarkup(row_width=1).add(sub_link, sub_btn)
