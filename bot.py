import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from database import check_and_update_user

logging.basicConfig(level=logging.INFO)
TOKEN = "8724671069:AAEBl86PVIx0HVRwwLAZK9dnkMmDvx_jljk"

JOKES = [
    "— Дорогой, я купила туфли! Всего за 200 евро!\n— И как они?\n— Ну, дома померяла — вроде ничего. А на улице в них почему-то начинают подкашиваться ноги и хочется выпить водки.",
    "Программист ложится спать. Жена говорит ему:\n— Закрой окно на ночь.\nВстает, компилирует код, ложится обратно.",
    "Встречаются два друга:\n— Как дела? Говорят, ты женился?\n— Да.\n— И как жена? Готовить умеет?\n— Ну, пельмени варит так, что аж во рту тают... правда, пока варит, сжечь успевает кастрюлю.",
    "Решил я как-то заняться спортом. Купил абонемент в фитнес-клуб. Теперь хожу туда... мысленно. И знаете, уже чувствую прилив сил!"
]

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(F.new_chat_members)
async def on_user_joined(message: Message):
    for user in message.new_chat_members:
        if user.id == (await bot.get_me()).id:
            continue
        
        check_and_update_user(user.id, user.username or "", user.first_name)
        await message.answer(
            f"Добро пожаловать в группу, {user.first_name}! 🎉\nМы рады видеть нового участника."
        )

@dp.message(F.text)
async def handle_all_messages(message: Message):
    if message.text.startswith("/"):
        return
        
    user = message.from_user
    if not user or user.is_bot:
        return

    status = check_and_update_user(user.id, user.username or "", user.first_name)

    if status == "returned":
        await message.answer(f"Привет, {user.first_name}! Рад снова тебя читать! 👋")
    elif random.randint(1, 20) == 1:
        joke = random.choice(JOKES)
        await message.answer(f"Кстати, к слову пришлось:\n\n{joke}")

@dp.message(F.text == "/joke")
async def send_joke_command(message: Message):
    joke = random.choice(JOKES)
    await message.answer(joke)

async def main():
    print("Бот 'Хранитель чата' запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())