from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

import bot_telegram.lib.db_scripts as dbscripts
from bot_telegram.lib.dbcommon import BaseSignals, Person
import bot_telegram.lib.telegram_bot_scripts as scripts
from bot_trading.lib.db.db_main import DB_str_n_one, Signals

router = Router()

class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()

@router.message(Command("upload_signals"))
async def cmd_upload_signals(message: Message, state: FSMContext):
    await message.answer(
        text="Напечатайте сигналы боту:"
    )
    await state.set_state(OrderFood.choosing_food_name)

@router.message(OrderFood.choosing_food_name)
async def food_chosen(message: Message, state: FSMContext):
    user_data = message.text

    global_query_lst = scripts.text_parser(user_data)
    # global_query_lst =[{'ticker': 'SBER', 'type_signal': 'Лонг', 'level_in': 194.0, 'support1': 190.0},
    #  {'ticker': 'PLZL', 'type_signal': 'Лонг', 'level_in': 9400.0},
    #  {'ticker': 'GAZP', 'type_signal': 'Лонг', 'level_in': 164.0, 'support1': 163.0, 'support2': 162.0},
    #  {'ticker': 'TATN', 'type_signal': 'Лонг', 'level_in': 347.0, 'support1': 345.0, 'support2': 343.0},
    #  {'ticker': 'ROSN', 'type_signal': 'Лонг', 'level_in': 365.0, 'support1': 363.0, 'support2': 360.0},
    #  {'ticker': 'MTLR', 'type_signal': 'Лонг', 'level_in': 141.0, 'support1': 140.0},
    #  {'ticker': 'OZON', 'type_signal': 'Лонг', 'level_in': 1700.0, 'support1': 1980.0},
    #  {'ticker': 'YNDX', 'type_signal': 'Лонг', 'level_in': 1900.0, 'support1': 1880.0}]

    # print(global_query_lst)

    dbscripts.base_clear_all(Signals)

    dbscripts.base_upload_signals_base(global_query_lst)

    dbscripts.base_upload_signals_to_strategies(global_query_lst, version=1)
    # dbscripts.base_upload_signals_to_strategies(global_query_lst, version=2)

    # dbscripts.base_upload_str_num_one(global_query_lst)

    data_from_base = dbscripts.base_show(Signals)

    result_from_telegram, result_for_panda = scripts.text_telegram_result(data_from_base)
    results_from_panda = scripts.data_to_panda(result_for_panda)


    result_telegram_str = ""
    for x in result_from_telegram:
        for y in x:
            result_telegram_str += str(y) + "   "
        result_telegram_str += "\n"

    # await message.answer(
    #     text=f"Сигналы приняты.\n"
    #          f"Нажмите на ссылку, чтобы проверить как их понял бот: /None"
    #          f"\n\n"
    #          f"Дальше должны быть результаты, но я их закомментировал"
    #          # f"{results_from_panda}"
    #          f"\n\n"
    #          # f"{result_telegram_str}"
    #         ,
    #     reply_markup=ReplyKeyboardRemove()
    # )
    # await state.clear()


    print("\n\n")
    print(results_from_panda)
    # print("\n\n")
    # print(*result_from_telegram)


