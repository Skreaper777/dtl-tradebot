from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from other.telegram_bots.mastergroosha.from_github.n07_fsm.keyboards.simple_row import make_row_keyboard
# from aiogram.utils.keyboard import make_row_keyboard

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
# available_food_names = ["Суши", "Спагетти", "Хачапури"]
# available_food_sizes = ["Маленькую", "Среднюю", "Большую"]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


@router.message(Command("food"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Напечатайте сигналы боту:"
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_food_name)

# Этап выбора блюда #


@router.message(OrderFood.choosing_food_name)
async def food_chosen(message: Message, state: FSMContext):
    # user_data = await state.get_data()
    user_data = message.text.lower()
    result_data = text_parser(user_data)


    # data = user_data.split("\n")
    # print(data)
    # result_data = []
    # for x in data:
    #     y = x.split()
    #     for key, value in ticker_dict.items():
    #         if value.find(y[0]) > -1:
    #             result_data.append(key)


    # result_data
    await message.answer(
        # text=f"Вы выбрали {message.text.lower()} порцию .\n"
        #      f"Попробуйте теперь заказать напитки: /drinks",
        text=f"Сигналы приняты.\n"
             f"Нажмите на ссылку, чтобы проверить как их понял бот: /drinks"
             f"{result_data}"
            ,
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()



def text_parser(data):
    ticker_dict = {"SBER": "Сбер", "GAZP": "Газпром", "RUAL": "Русал", "TATN": "Татнефть", "PHOR": "Фосагро",
                   "FIVE": "Х5", "YNDX": "Яша"}
    data = data.split("\n")
    temp_data = []
    for xi, x in enumerate(data):
        temp_data.append([])
        napr_sdelki = 0
        lvl_vhod = 0
        lomanaya_stroka = 0
        name_uroven1 = 0
        name_uroven2 = 0
        for i, y in enumerate(x.split()):
            if not lomanaya_stroka:
                y = y.lower()
                if y[-1] == "." or y[-1] == ",":
                    y = y[:-1]
                if y[0] == "." or y[0] == ",":
                    y = y[1:]
                # print(set(y))
                if set(y) < {'0','1','2','3','4','5','6','7','8','9','.',','}:

                    y = float(y.replace(",","."))
                if i == 0:
                    for key, value in ticker_dict.items():
                        if value.lower().find(y.lower()) > -1:
                            temp_data[xi].append(key)
                elif y == "шорт" and not napr_sdelki:
                    temp_data[xi].append("Шорт")
                    napr_sdelki = 1
                elif y == "лонг" and not napr_sdelki:
                    temp_data[xi].append("Лонг")
                    napr_sdelki = 1
                elif not napr_sdelki and not lvl_vhod and type(y) == float:
                    temp_data[xi].append("Неизвестно")
                    napr_sdelki = 1
                    lomanaya_stroka = 1
                elif napr_sdelki and not lvl_vhod and type(y) == float:
                    temp_data[xi].append(float(y))
                    lvl_vhod = 1
                elif napr_sdelki and lvl_vhod and type(y) != float and not name_uroven1:
                    if y == "под":
                        temp_data[xi].append("Поддержка")
                        name_uroven1 = 1
                    elif y == "сопр":
                        temp_data[xi].append("Сопротивление")
                        name_uroven1 = 1
                elif name_uroven1 and type(y) == float:
                    temp_data[xi].append(float(y))
                elif name_uroven1 and type(y) != float and not name_uroven2:
                    if y == "под":
                        temp_data[xi].append("Поддержка")
                        name_uroven2 = 1
                    elif y == "сопр":
                        temp_data[xi].append("Сопротивление")
                        name_uroven2 = 1

                    # print(temp_data)
        # for y in x.split():
    # print("done", temp_data)
    return temp_data

# @router.message(OrderFood.choosing_food_name)
# async def food_chosen_incorrectly(message: Message):
#     await message.answer(
#         text="Я не знаю такого блюда.\n\n"
#              "Пожалуйста, выберите одно из названий из списка ниже:",
#         reply_markup=make_row_keyboard(available_food_names)
#     )
#
# # Этап выбора размера порции и отображение сводной информации #
#



# @router.message(OrderFood.choosing_food_size)
# async def food_size_chosen(message: Message, state: FSMContext):
#     user_data = await state.get_data()
#     await message.answer(
#         text=f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
#              f"Попробуйте теперь заказать напитки: /drinks",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     # Сброс состояния и сохранённых данных у пользователя
#     await state.clear()
#
#
# @router.message(OrderFood.choosing_food_size)
# async def food_size_chosen_incorrectly(message: Message):
#     await message.answer(
#         text="Я не знаю такого размера порции.\n\n"
#              "Пожалуйста, выберите один из вариантов из списка ниже:",
#         reply_markup=make_row_keyboard(available_food_sizes)
#     )
