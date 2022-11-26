from aiogram.dispatcher.filters.state import StatesGroup, State

class Sub(StatesGroup):
    link = State()

class Enable_sub(StatesGroup):
    choices = State()

class Cartoon(StatesGroup):
    sezon = State()
    count = State()
    chapters = State()

class GetCartoon(StatesGroup):
    sezon = State()
    chapter = State()

class Ad(StatesGroup):
    text = State()

class AddChap(StatesGroup):
    sezon = State()
    chapter = State()