import logging

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from scrap import get_users, send

logging.basicConfig(level=logging.INFO)

bot = Bot(token='')
dp = Dispatcher(bot, storage=MemoryStorage())


class GROUP(StatesGroup):
    group = State()
    text = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(text='Введите ссылку на группу...')
    await GROUP.group.set()


@dp.message_handler(state=GROUP.group)
async def group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await message.answer(text='теперь введите текст рассылки...')
    await GROUP.next()


@dp.message_handler(state=GROUP.text)
async def text(message: types.Message, state: FSMContext):
    await message.answer('Рассылка начата...')
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.finish()
    try:
        await get_users(data['group'])
        await send(data['text'])
    except:
        await message.answer('Ошибка исполнения программы, для просмотра лога ошибки перезапустите скрипт на пк')
    await message.answer("Работа завершена")

if __name__ == '__main__':
    executor.start_polling(dp)