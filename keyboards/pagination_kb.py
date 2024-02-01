from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.file_handling import book



def pagination_kbrd(func):
    def wrapper(page: int = 1):
        middle_btn = f"{page}/{len(book)}"
        if page == 1:
            return func(middle_btn, 'forward')
        elif page > 1 and page < len(book):
            return func('backward', middle_btn, 'forward')
        else:
            return func('backward', middle_btn)
    return wrapper


@pagination_kbrd
def create_pagination_keyboard(*buttons):
    pagination_kbuilder = InlineKeyboardBuilder()
    pagination_kbuilder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons])
    return pagination_kbuilder.as_markup()