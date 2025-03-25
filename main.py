from aiogram import Bot, Dispatcher, executor , types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

TOKEN = "8175468014:AAHHXenesmv8On1hEN1MpizpN3PzZdvgG7k"


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage= MemoryStorage())
admins = [6428277280]


shaxzod = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Sherik kerak"), KeyboardButton(text="Ish joyi kerak")],
        [KeyboardButton(text="Hodim kerak"), KeyboardButton("Ustoz kerak")],
        [KeyboardButton("Shogird kerak")]
    ],
    resize_keyboard=True
)

confirm_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Yes", callback_data="confirm_yes"), InlineKeyboardButton(text="No",callback_data="confirm_no")]
    ]
)

class ShogirtState(StatesGroup):
    fullname = State()
    age = State()
    texnologiya = State()
    contact = State()


async def on_startup(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")
        except (Exception) as err:
            pass


@dp.message_handler(commands=['start','help'])
async def start_func(message: types.Message):
    if message.text == "/start":
        await message.reply(f"""<b>Assalom alaykum {message.from_user.full_name}
UstozShogird kanalining rasmiy botiga xush kelibsiz!</b>

/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!""", reply_markup=shaxzod)
    else:
        await message.reply(f"Yordam olish uchun admin bilan bog'laning")

@dp.message_handler(text = "Shogird kerak")
async def shogird_func(message: types.Message):
    await message.answer(text="""<b>Shogird topish uchun ariza berish</b>

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""")
    await message.answer("<b>Ism, familiyangizni kiriting?:</b>")
    await ShogirtState.fullname.set()

@dp.message_handler(state=ShogirtState.fullname)
async def set_name(message: types.Message, state:FSMContext):
    await state.update_data(fullname = message.text)
    await message.answer("Yoshingni kirit:")
    await ShogirtState.age.set()

@dp.message_handler(state=ShogirtState.age)
async def set_age(message: types.Message, state:FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Texnologiya kirit:")
    await ShogirtState.texnologiya.set()


@dp.message_handler(state=ShogirtState.texnologiya)
async def set_texnologiya(message: types.Message, state:FSMContext):
    await state.update_data(texnologiya = message.text)
    await message.answer("Kontakt kirit: ")
    await ShogirtState.contact.set()

@dp.message_handler(state=ShogirtState.contact)
async def set_kontakt(message: types.Message, state:FSMContext):
    await state.update_data(contact = message.text)
    
    user_data = await state.get_data()

    text = f"""Sizning malumotlaringiz:
    
Nomi: {user_data['fullname']},
Yoshi: {user_data["age"]},
Texnologiya: {user_data['texnologiya']},
Kontakt: {user_data["contact"]}"""

    await message.answer(text= text, reply_markup=confirm_btn)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
