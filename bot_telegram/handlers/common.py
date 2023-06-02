from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove




router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    # await message.answer(
    #     text="Выберите, что хотите заказать: "
    #          "блюда (/food) или напитки (/drinks).",
    #     reply_markup=ReplyKeyboardRemove()
    # )
    await message.answer(
        text="Выберите настройку",
        # reply_markup=ReplyKeyboardRemove()
        reply_markup=get_keyboard_start()
    )

@router.message(Command("cancel"))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


def get_keyboard_start():
    buttons = [
        [types.InlineKeyboardButton(text="Загрузить сигналы", callback_data="upload_signals_pre")],
        [types.InlineKeyboardButton(text="Состояние бота", callback_data="setting_bot")],
        [types.InlineKeyboardButton(text="Передать информацию боту", callback_data="set_bot")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@router.callback_query(Text("setting_bot"))
async def send_setting_bot(callback: types.CallbackQuery):
    # await message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    # await callback.message.answer(str(randint(1, 10)))
    await callback.message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    await callback.answer(
        text="Вы изменили настройки бота",
        show_alert=True
    )
    # или просто await call.answer()

@router.callback_query(Text("upload_signals_pre"))
async def send_set_bot(callback: types.CallbackQuery):
    # await message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    # await callback.message.answer(str(randint(1, 10)))
    await callback.message.answer("/upload_signals")
    # await callback.answer(
    #     text="/food",
    #     show_alert=True
    # )
    # или просто await call.answer()

@router.message(Command("food2"))
async def send_food2(callback: types.CallbackQuery):
    # await message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    # await callback.message.answer(str(randint(1, 10)))
    await callback.message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    await callback.answer(
        text="Вы изменили настройки бота",
        show_alert=True
    )
    # или просто await call.answer()


def get_keyboard_settings():
    buttons = [
        [types.InlineKeyboardButton(text="Задать бумаги", callback_data="setting_bot")],
        [types.InlineKeyboardButton(text="Изменить бумаги", callback_data="setting_bot")],
        [types.InlineKeyboardButton(text="Обнулить настройки", callback_data="setting_bot")]
        # [types.InlineKeyboardButton(text="Вернуться назад", callback_data="start")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard