
from itertools import count
from aiogram import Bot, Dispatcher, executor, types
import logging
from config import TOKEN, CLOUDID
from db import Sqlite
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from states import Sub, Enable_sub, Cartoon, GetCartoon, Ad, AddChap
import btn
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
db = Sqlite('rick.db')
ad_link = '@tiktopgirl'
sub = True
chapter_count = []

@dp.message_handler(commands='chapter')
async def add_chapter(message: types.Message):
    await message.answer('Выберите сезон', reply_markup=btn.sezon_creation(db.get_sezon()))
    await AddChap.sezon.set()

@dp.message_handler(state= AddChap.sezon)
async def add_chapter2(message: types.Message, state: FSMContext):
    await state.update_data(sezon = message.text)
    await state.update_data(count = db.get_count(message.text)[0])
    await message.answer(f'Отправьте {db.get_count(message.text)[0] + 1} серию')
    await AddChap.chapter.set()

@dp.message_handler(state=AddChap.chapter, content_types='video')
async def add_chapter3(message: types.Message, state: FSMContext):
    response = requests.post(
        url=f'https://api.telegram.org/bot{TOKEN}/sendVideo',
        data={f'chat_id': {CLOUDID}, 'video': message.video.file_id}
    ).json()
    data = await state.get_data()
    count = int(data['count']) +1
    db.add_cartoon(response['result']['message_id'], data['sezon'], count)
    db.update_sezon(data['sezon'], count)
    await message.answer('Готово')
    await state.finish()

@dp.message_handler(commands='stats')
async def stats(message: types.Message):
    await message.answer(f'{len(db.get_user())} - пользователей используют бота')


@dp.message_handler(commands='ad')
async def ad(message: types.Message):
    await message.answer("Отправьте текст")
    await Ad.text.set()

@dp.message_handler(state=Ad.text)
async def ad2(message: types.Message, state: FSMContext):
    for user in db.get_user():
        await bot.send_message(user[0], message.text)
    await message.answer('Готово')
    await state.finish()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    db.add_users(message.from_user.id)
    if sub == False:
        await message.answer('Привет! Этот бот предназначен для скачивания и просмотра мульт. сериала "Рик и Морти"', reply_markup=btn.sezon_creation(db.get_sezon()))
    if sub == True:
        await message.answer('Для продолжения требуется подписка на канал',reply_markup=btn.ad_menu)


@dp.message_handler(text='Назад', state='*')
async def back(message: types.Message, state: FSMContext):
    await message.answer('Главная Страница', reply_markup=btn.sezon_creation(db.get_sezon()))
    await state.finish()

@dp.callback_query_handler(lambda c: c.data ==  'done')
async def done_check(call: types.CallbackQuery):
    user_channel_status = await bot.get_chat_member(chat_id=ad_link, user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        await bot.send_message(call.from_user.id, 'Выберите сезон', reply_markup=btn.sezon_creation(db.get_sezon()))
    else:
        await bot.answer_callback_query(callback_query_id=call.id,text='Для доступа подпишитесь на канал',show_alert=True)


# get cartoon

@dp.message_handler(text=db.get_sezon())
async def get_cartoon(message: types.Message):
    global sezon 
    sezon = message.text
    user_channel_status = await bot.get_chat_member(chat_id=ad_link, user_id=message.from_user.id)
    if sub == True:
        if user_channel_status["status"] != 'left':
            if message.text in db.get_sezon():
                count=db.get_count(message.text)
                await message.answer('Выберите серию', reply_markup= btn.btn_creator(count[0]))
                await GetCartoon.chapter.set()
            else:
                await message.answer('Извините, выберите сезон из нижеследующего', reply_markup=btn.sezon_creation(db.get_sezon()))
        if user_channel_status["status"] == 'left':
            await message.answer('Для продолжения требуется подписка на канал',reply_markup=btn.ad_menu_sez)
    if sub == False:
        if int(message.text) in db.get_sezon():
            count=db.get_count(message.text)
            await message.answer('Выберите серию', reply_markup= btn.btn_creator(count[0]))
            await GetCartoon.chapter.set()
        else:
                await message.answer('Извините, выберите сезон из нижеследующего', reply_markup=btn.sezon_creation(db.get_sezon()))


@dp.message_handler(state=GetCartoon.chapter)
async def get_chapter(message: types.Message, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id=ad_link, user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        chapter = message.text
        cartoon = db.get_cartoon(sezon,chapter)
        response = requests.post(
            url=f'https://api.telegram.org/bot{TOKEN}/forwardMessage',
            data={f'chat_id': {message.from_user.id}, 'from_chat_id': {CLOUDID}, 'message_id': {cartoon[0]}}
        ).json()

    if user_channel_status["status"] == 'left':
        await message.answer('Для продолжения требуется подписка на канал',reply_markup=btn.ad_menu_sez)


@dp.callback_query_handler(lambda c: c.data ==  'done_sez')
async def done(call: types.CallbackQuery):
    count=db.get_count(sezon)
    user_channel_status = await bot.get_chat_member(chat_id=ad_link, user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        await bot.send_message(call.from_user.id,'Выберите серию', reply_markup= btn.btn_creator(count[0]))
        await GetCartoon.chapter.set()
    else:
        await bot.answer_callback_query(callback_query_id=call.id,text='Для доступа подпишитесь на канал',show_alert=True)
#add cartoon  

@dp.message_handler(commands='add')
async def add_cartoon(message: types.Message):
    await message.answer('Введите сезон')
    await Cartoon.sezon.set()

@dp.message_handler(state=Cartoon.sezon)
async def add_sezon(message: types.Message, state: FSMContext):
    await state.update_data(sezon = message.text)
    done = KeyboardButton('Готово')
    done_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(done)
    await message.answer("Отправьте серии в правильном порядке, и нажмите на кнопку ниже", reply_markup=done_menu)
    await Cartoon.chapters.set()

@dp.message_handler(state=Cartoon.chapters, content_types='video')
async def get_chapters(message: types.Message, state: FSMContext):

    response = requests.post(
        url=f'https://api.telegram.org/bot{TOKEN}/sendVideo',
        data={f'chat_id': {CLOUDID}, 'video': message.video.file_id}
    ).json()
    chapter_count.append(response['result']['message_id'])
    data = await state.get_data()
    db.add_cartoon(response['result']['message_id'], data['sezon'],len(chapter_count))

    
@dp.message_handler(state=Cartoon.chapters, text='Готово')
async def add_sezon(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db.add_sezon(data['sezon'], len(chapter_count))
    await message.answer('Готово, переход на страницу сезонов', reply_markup=btn.sezon_creation(db.get_sezon()))
    chapter_count.clear()
    await state.finish()

# enable or disable subscription

@dp.message_handler(commands='sub')
async def enable_sub(message: types.Message):
    await message.answer('Какое действие вы хотите совершить?', reply_markup=btn.sub_menu)
    await Enable_sub.choices.set()

@dp.message_handler(state=Enable_sub.choices)
async def enable_sub2(message: types.Message, state: FSMContext):
    global sub
    if message.text == "Вкл":        
        sub = True
    if message.text == "Выкл":
        sub = False
    await message.answer('Готово')
    await state.finish()


#add sub link

@dp.message_handler(commands='link')
async def add_sub(message: types.Message):
    await message.answer('Отпавьте ссылку')
    await Sub.link.set()

@dp.message_handler(state= Sub.link)
async def sub2(message: types.Message, state: FSMContext):
    global ad_link
    ad_link = message.text
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
