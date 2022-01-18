"""
Этот бот принимает сообщение и пересылает в телеграм канал или группу с указанным channel id
"""
import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit

#создадим переменнные окружения BOT_ID и CH_ID

bot_token = getenv("BOT_ID")
if not bot_token:
    exit("Error: no bot token provided")

channel_token = getenv("CH_ID")
if not channel_token:
    exit("Error: no channel token provided")

API_TOKEN = bot_token
CHANNEL_ID = channel_token
PHOTOS_ID = []

# Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Объект бота (его инициализация)
bot = Bot(token=API_TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)

from aiogram.utils.exceptions import BotBlocked

@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True

# Хэндлер на команду
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    `/start` или `/help`
    """
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns_text = ('Да!', 'Нет!')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    await message.reply("Привет!\nЯ бот пересылки фотографий и картинок в канал!")
    await message.answer("Готов присылать мне картинки?"
                       + ' {user}!'.format(user=message.from_user.full_name), reply_markup=keyboard_markup)

@dp.message_handler(content_types=["photo"])
async def send_photo(message: types.Message):
    """Переслать фото в канал"""
    photo_id = message.photo[-1].file_id

    #await bot.send_photo(message.from_user.id, photo_id, caption="Данная картинка была успешно переслана")
    await message.answer("Данная картинка была успешно переслана")
    #await bot.send_photo(message.from_user.id, "Данная картинка была успешно переслана")
    await bot.send_photo(CHANNEL_ID, photo_id, caption="Пересланная картинка")

@dp.message_handler()
async def all_msg_handler(message: types.Message):
    button_text = message.text
    logger.debug('The answer is %r', button_text)  

    if button_text == 'Да!':
        reply_text = "Отлично, присылай!!!"
    elif button_text == 'Нет!':
        reply_text = "О неет, что это?"
    else:
        reply_text = "Сохраняйте спокойствие ... Все в порядке"

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    #await bot.send_message(CHANNEL_ID, reply_text)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

