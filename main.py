import re
import json

from smtp_authorization import SMTPauthorizer

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# Read the secret data from env file
with open("env", "r") as f:
    secret = json.loads(f.read())
bot = Bot(token=secret['TG_TOKEN'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    name = msg.from_user.first_name
    await msg.answer(f"Helo, {name}. Enter your email. \n To confirm your identity we will send you a code. Please enter your email.")


@dp.message_handler(commands=['help'])
async def send_welcome(msg: types.Message):
    await msg.answer("""I can confirm your identity""")


so = SMTPauthorizer(secret)
@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if so.email_is_valid(msg.text.lower()):
        so.send_confirmation_code(email=msg.text.lower())
        await msg.answer(f'Email {msg.text.lower()} is valid! We sent code to you. Check your mail.')
    elif so.last_confirmation_code and so.confirm_email(code=msg.text.lower()):
        await msg.answer(f'Thank you! Your email is confirmed.')
    elif re.fullmatch(re.compile(r'[\d]{6}'), msg.text.lower()):
        await msg.answer(f'You entered a wrong code.')
    else:
        await msg.answer(f'Email {msg.text.lower()} is not valid! Try again.')


if __name__ == '__main__':
    executor.start_polling(dp)
