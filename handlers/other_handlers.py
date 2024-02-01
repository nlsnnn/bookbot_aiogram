from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON

other_router = Router()


@other_router.message()
async def other_msh(message: Message):
    await message.answer(f'Извините, но я не понимаю команду {message.text}. Пожалуйста, попробуйте еще раз или воспользуйтесь командой /help для получения дополнительной информации о доступных командах')
