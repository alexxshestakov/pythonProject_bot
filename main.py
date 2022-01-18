"""
Этот бот принимает сообщение и пересылает в телеграм канал или группу с указанным channel id
"""

''' импорт библиотек'''
import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode

#создадим переменнные окружения BOT_ID и CH_ID
bot_token = getenv("BOT_ID")
if not bot_token:
    exit("Error: no bot token provided")

channel_token = getenv("CH_ID")
if not channel_token:
    exit("Error: no channel token provided")

API_TOKEN = bot_token
CHANNEL_ID = channel_token

# Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Объект бота (его инициализация)
bot = Bot(token=API_TOKEN)
# Диспетчер бота
dp = Dispatcher(bot)

# Хэндлер на команду start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    `/start` или `/help`
    """
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns_text = ('Да!', 'Нет!')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    await message.reply("Привет!👋\nЯ бот 🤖 пересылки фотографий и картинок в канал!")
    await message.answer("Готов присылать мне картинки?"
                       + ' {user}!'.format(user=message.from_user.full_name), reply_markup=keyboard_markup)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу 😎 ответить на следующие команды:'),
               '/start - старт', '/dice - бросить игральную кость', '/help - помощь', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")

@dp.message_handler()
async def all_msg_handler(message: types.Message):
    button_text = message.text
    logger.debug('The answer is %r', button_text)

    if button_text == 'Да!':
        reply_text = "Отлично, присылай 😇 !!!"
    elif button_text == 'Нет!':
        reply_text = " О нет, почему расхотел ? 👀\nЕсли захочешь снова жми /start "
    elif button_text.lower() in ['привет', 'прив', 'hi', 'Hello', '']:
        reply_text = " Привет! 👋\nЯ бот 🤖 пересылки фотографий и картинок в канал!\nЖми /start "
    elif button_text.lower() in ['пока', 'bye', 'goodbye']:
        reply_text = " Возвращайся 😕"
    else:
        reply_text = "Сохраняйте спокойствие 👐 ... Все в порядке👍.\nЧтобы начать снова отправьте боту команду /start"

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(content_types=["photo"])
async def send_photo(message: types.Message):
    """Переслать фото в канал"""
    date = message.date  # ДАТА, ВРЕМЯ ОТПРАВКИ СООБЩЕНИЯ
    photo_id = message.photo[-1].file_id
    rep_text = message.text
    await message.answer("Данная картинка была успешно переслана в канал 👌")
    await bot.send_photo(CHANNEL_ID, photo_id, caption='Данная картинка переслана ботом 🤖')

'''Запуск бота'''
if __name__ == '__main__':
    '''необходимо для того, чтобы бот работал постоянно '''
    executor.start_polling(dp, skip_updates=True)

