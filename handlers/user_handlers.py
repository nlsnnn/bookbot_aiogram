from copy import deepcopy
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import (create_edit_keyboard, create_bookmarks_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book


router = Router()



@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(text=LEXICON['/start'])
    if message.chat.id not in users_db:
        users_db[message.chat.id] = deepcopy(user_dict_template)


@router.message(Command(commands='help'))
async def help_cmd(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands='beginning'))
async def beginning_cmd(message: Message):
    users_db[message.chat.id]['page'] = 1
    text = book[users_db[message.chat.id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_keyboard(
                             users_db[message.chat.id]['page']
                         ))


@router.message(Command(commands='continue'))
async def continue_cmd(message: Message):
    text = book[users_db[message.chat.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            users_db[message.chat.id]['page']
        ))


@router.message(Command(commands='bookmarks'))
async def bookmarks_cmd(message: Message):
    if users_db[message.chat.id]['bookmarks']:
        await message.answer(
            text=LEXICON['/bookmarks'],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.chat.id]['bookmarks']
                ))
    else:
        await message.answer(LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                users_db[callback.from_user.id]['page']
            ))
    else:
        await callback.answer(text='Больше страниц нет')


@router.callback_query(F.data == 'backward')
async def backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                users_db[callback.from_user.id]['page']
            ))
    else:
        await callback.answer(text='Ты на первой странице!')


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer("Страница добавлена в закладки!")


@router.callback_query(IsDigitCallbackData())
async def bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            users_db[callback.from_user.id]['page']
        ))
    await callback.answer()


@router.callback_query(F.data == "edit_bookmarks")
async def edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_edit_keyboard(*users_db[callback.from_user.id]['bookmarks'])
    )
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmark(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_bookmarks_keyboard(
                *users_db[callback.from_user.id]['bookmarks'])
        )
    else:
        await callback.message.edit_text(LEXICON['no_bookmarks'])
    await callback.answer()