import bot_trading.lib.db.db_main as dbmain
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float

import bot_trading.lib.utilities.main_utilities as utilities

# engine = dbmain.base_connecter()

class Orders:
    def __init__(self):
        self.open_orders = False

    def get_open_orders(self):
        """
        Открытые ордера или частично исполненные

            orders = client.orders.get_orders(account_id="a9d1b0b4-af34-44e9-b556-9ee9fa82d511").orders
            # print(orders)
            # print(client.orders.get_orders())
            # не исполненные заявки можно отменить
            # order_id = orders[0].order_id
            # print("Lets cancel order w id %s" % order_id)
            # r = client.orders.cancel_order(account_id=creds.account_id_test, order_id=order_id)
            # print(r)

        :return:
        """
        self.open_orders = self.get_open_orders_sandbox()
        return self.open_orders
        # return False

    def set_open_orders(self, status):
        self.open_orders = status

    @staticmethod
    def open_ticket_buy():
        """
        Вхожу в лонг

        :return:
        """

        with Session(autoflush=False, bind=engine) as db:
            # создаем объект Person для добавления в бд
            tom = dbmain.Person(figi='BBG004730N88', ticker_name=utilities.Utility.convert_figi_to_ticker('BBG004730N88'), type_order='long',
                                open_ticker_price=100.82, time_create=utilities.Utility.current_moscow_time())
            db.add(tom)  # добавляем в бд
            db.commit()  # сохраняем изменения

        utilities.Utility.otladka_print(txt="вхожу в сделку на лонг", type_msg=1, lvl=1)
        return True

    @staticmethod
    def open_ticket_sell():
        """
        Вхожу в шорт

        :return:
        """

        utilities.Utility.otladka_print(txt="вхожу в сделку на шорт", type_msg=1, lvl=1)
        return True

    def get_open_orders_sandbox(self):
        """
        Получение открытых сделок в песочнице

        :return:
        """
        with Session(autoflush=False, bind=engine) as db:
            result = db.query(dbmain.Person).filter(dbmain.Person.figi == 'BBG004730N88').all()
            if len(result) == 1:
                return True
            elif len(result) > 1:
                utilities.Utility.otladka_print(txt="ОШИБКА: В базе данных более одной записи о сделке.", lvl=1)
                return True
            elif len(result) == 0:
                utilities.Utility.otladka_print(txt="В базе данных нет записи о сделках с таким тикером", lvl=1)
                return False
