import asyncio
import logging
import sys
from os import getenv

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
from aiogram.utils.i18n import gettext as _, I18n, FSMI18nMiddleware
from aiogram.utils.i18n import lazy_gettext as __

load_dotenv(r"C:\Users\begzo\PycharmProjects\Bot\.env")

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, state
from aiogram.types import Message, KeyboardButton

TOKEN = getenv("TOKEN")

dp = Dispatcher()

class ButtonState(StatesGroup):
    lang = State()

class ChatState(StatesGroup):
    Stop = State()

def make_btn(btn_name: list, adjust: list):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=name) for name in btn_name])
    rkb.adjust(*adjust)
    return rkb.as_markup(resize_keyboard=True, one_time_keyboard=True)

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    btn_name = [_("Chat boshlash 🤗"), _("Bot Haqida 🤖"), _("🇺🇿/🇺🇸 Til")]
    adjust = [2]
    photo = "https://play-lh.googleusercontent.com/29QZt9UmwW5g0foe7csUIHsKbF6EJSlzQ0gjFajymHuUSzXyl0eobYcuwwfwr4mi2_i-"
    await message.answer(_(f"Salom, {html.bold(message.from_user.full_name)} 👋 Anonim chatga hush kelibsiz !"),
                         reply_markup=make_btn(btn_name, adjust))
    await message.answer_photo(photo, caption=_("👥 Siz bu botda odamlar bilan tanish imkonyatiga egasiz !"))

@dp.message(F.text == "Chat boshlash 🤗")
async def chat_handler(message: Message, state : FSMContext) -> None:
    await message.answer(_("Siz suhbatdoshni kutyapsiz 🫂, Bir oz kuting 🙏"))
    waiting_list = []
    for user in waiting_list:
        waiting_list.append(user)
        if user in waiting_list and waiting_list[user] % 2 == 0:
            await message.answer(_("Siz suhbatdosh bilan bog'landiniz 🥂, Endi yozishni boshlashingiz mumkin 🖊"))

@dp.message(ChatState.Stop, F.text == "Ortga 🔙")
@dp.message(F.text == "Chat boshlash 🤗")
async def btn_handler_1(message: Message, state : FSMContext) -> None:
    btn_name = [_("Chatni tugatish 🛑") , _("Ortga 🔙")]
    adjust = [2]
    await state.set_state(ChatState.Stop)
    await message.answer(_(f"Suhbat tugatildi yangi suhbatni boshlash uchun [Chat boshlash 🤗] tugmasini bosing !"),
                         reply_markup=make_btn(btn_name, adjust))


@dp.message(F.text == "Bot Haqida 🤖")
async def about_bot_handler(message: Message) -> None:
    await message.answer(_("Bu botda siz o'zga insonlar bilan muloqot qila olasiz 🤩 shunchaki [Chat boshlash 🤗]"
" 👈🏻 tugmasini bosing va odamlar bilan muloqot qiling!"))

@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer("How can i help you?")


@dp.message(F.text == __("🇺🇿/🇺🇸 Til"))
async def lang_handler(message : Message , state : FSMContext):
    btns = ["🇺🇿 O'zbekcha" , "🇺🇸 English" , _("Ortga ")]
    ad_just = [2]
    await state.set_state(ButtonState.lang)
    await message.answer(_("Maqul tilni tanlang !") , reply_markup=make_btn(btns , ad_just))


@dp.message(ButtonState.lang)
async def lang_handler(message : Message , state : FSMContext , i18n):
    lang = {

        "🇺🇿 O'zbekcha" : "uz",
        "🇺🇸 English" : "en",

    }
    code = lang.get(message.text)
    await state.set_data({"locale" :code })
    i18n.current_locale = code
    btns = [
        _("Chat boshlash 🤗"),
        _("Bot Haqida 🤖"),
        _("🇺🇿/🇺🇸 Til")
    ]
    ad_just = [2, 1]
    await message.answer(_("Til o'zgardi !") , reply_markup=make_btn(btns , ad_just))

async def main() -> None:
    i18n = I18n(path=r"C:\Users\begzo\PycharmProjects\Bot\locales", default_locale="uz", domain="messages")
    dp.update.middleware(FSMI18nMiddleware(i18n))
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

# 👀 Ustoz agar o'qisez mana bu 👉🏻 path=r"C:\Users\begzo\PycharmProjects\Bot\locales" siz ishlamapti locale qisam ishlamadi
# shu uchun ozimi pazimi yozdim 🙏🏻

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())