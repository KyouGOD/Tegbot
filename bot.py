from config import TOKEN
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

URL = 'https://ru.investing.com/currencies/usd-rub'
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
driver.get(URL)
element = driver.find_element("xpath", "/html/body/div[1]/div[2]/div/div/div[2]/main/div/div[1]/div[2]/div[1]/span")
print('Browser Started')


def get_course():
    course = str(BeautifulSoup(element.text, "html.parser"))
    return float(course.replace(',', '.'))


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class FSMBounds(StatesGroup):
    lower_bound = State()
    upper_bound = State()


async def on_startup(_):
    print('Bot Online')


async def cycle(data, message):
    while True:
        print("Im still working")
        if get_course() < data["lower_bound"] or get_course() > data["upper_bound"]:
            if get_course() < data["lower_bound"]:
                await message.answer("Курс вышел за нижний предел")
                break
            elif get_course() > data["upper_bound"]:
                await message.answer("Курс вышел за верхний предел")
                break
            break
        await asyncio.sleep(1)


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await message.reply(
        "Бот отслеживания курса валютной пары \nUSD/RUB на Московской бирже.\nТорги открываются в 7:00 по"
        " московскому времени.\nТорги закрываются в 19:00 по московскому времени.\nВы можете установи"
        "ть границы курса до 4 знаков после запятой, при выходе из которых вы получите уведомление.\nДос"
        "тупные команды:\n/start\n/help\n/bounds\n/currentcourse")


@dp.message_handler(commands=['currentcourse'])
async def print_course(message: types.Message):
    await message.answer(f'Текущий курс USD/RUB: {get_course()}')


@dp.message_handler(commands=['bounds'])
async def cmd_bounds(message: types.Message):
    await FSMBounds.lower_bound.set()
    await message.answer('Введите нижнюю границу')


@dp.message_handler(state=FSMBounds.lower_bound)
async def get_lower_bound(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lower_bound'] = float(message.text)
    await FSMBounds.next()
    await message.answer('Введите верхнюю границу')


@dp.message_handler(state=FSMBounds.upper_bound)
async def get_upper_bound(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['upper_bound'] = float(message.text)
    async with state.proxy() as data:
        await message.answer(f'Границы сохранены.\nВерхняя граница: {data["lower_bound"]}\nНижняя граница: {data["upper_bound"]}')
    asyncio.create_task(cycle(data, message))
    await state.finish()


@dp.message_handler()
async def no_cmd(message: types.Message):
    await message.answer('Нет такой команды')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
