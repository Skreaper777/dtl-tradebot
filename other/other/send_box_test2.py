""" Example - How to set/get balance for sandbox account.
    How to get/close all sandbox accounts.
    How to open new sandbox account. """

import logging
import os
from datetime import datetime
from decimal import Decimal

from tinkoff.invest import Client, MoneyValue
from tinkoff.invest.utils import decimal_to_quotation, quotation_to_decimal

# TOKEN = os.environ["INVEST_TOKEN"]
TOKEN = 't.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg' # Токен для песочницы


logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def add_money_sandbox(client, account_id, money, currency="rub"):
    """Function to add money to sandbox account."""
    money = decimal_to_quotation(Decimal(money))
    return client.sandbox.sandbox_pay_in(
        account_id=account_id,
        amount=MoneyValue(units=money.units, nano=money.nano, currency=currency),
    )


def main():
    """Example - How to set/get balance for sandbox account.
    How to get/close all sandbox accounts.
    How to open new sandbox account."""
    with Client(TOKEN) as client:
        #a9d1b0b4-af34-44e9-b556-9ee9fa82d511 Текущий ID  в песочнице

        # get all sandbox accounts
        sandbox_accounts = client.sandbox.get_sandbox_accounts()
        print("Вот все счета в песочнице", sandbox_accounts)

        # close all sandbox accounts
        # for sandbox_account in sandbox_accounts.accounts:
        #     client.sandbox.close_sandbox_account(account_id=sandbox_account.id)
        # client.sandbox.close_sandbox_account(account_id="5d67e7c4-8bc6-44e0-917f-707bd7a1c77e")



        # open new sandbox account
        # sandbox_account = client.sandbox.open_sandbox_account()

        # print("??????", sandbox_accounts['accounts'])

        # print("11111", type(sandbox_accounts.accounts)) #list
        # print("22222", type(sandbox_accounts.accounts[0])) #tinkoff.invest.schemas.Account

        # print("00000", sandbox_accounts)
        # print("11111", sandbox_accounts.accounts)
        # print("22222", sandbox_accounts.accounts[0])
        #
        # print("33333", sandbox_accounts.accounts[0].id)

        # print("!!!!!", sandbox_accounts.accounts.__dict__)

        # print("Открытие нового счета", sandbox_account.account_id)
        # print("ID аккаунта", sandbox_account.account_id)

        # account_id = sandbox_account.account_id

        account_id = sandbox_accounts.accounts[0].id

        # add initial 2 000 000 to sandbox account
        print(add_money_sandbox(client=client, account_id=account_id, money=2000000))
        logger.info(
            "positions: %s", client.sandbox.get_sandbox_positions(account_id=account_id)
        )
        print(
            "money: ",
            float(
                quotation_to_decimal(
                    client.sandbox.get_sandbox_positions(account_id=account_id).money[0]
                )
            ),
        )

        logger.info(
            "orders: %s", client.sandbox.get_sandbox_orders(account_id=account_id)
        )
        logger.info(
            "positions: %s", client.sandbox.get_sandbox_positions(account_id=account_id)
        )
        logger.info(
            "portfolio: %s", client.sandbox.get_sandbox_portfolio(account_id=account_id)
        )
        logger.info(
            "operations: %s",
            client.sandbox.get_sandbox_operations(
                account_id=account_id,
                from_=datetime(2023, 1, 1),
                to=datetime(2023, 2, 5),
            ),
        )
        logger.info(
            "withdraw_limits: %s",
            client.sandbox.get_sandbox_withdraw_limits(account_id=account_id),
        )

        # add + 2 000 000 to sandbox account, total is 4 000 000
        print(add_money_sandbox(client=client, account_id=account_id, money=2000000))
        logger.info(
            "positions: %s", client.sandbox.get_sandbox_positions(account_id=account_id)
        )

        # close new sandbox account
        # sandbox_account = client.sandbox.close_sandbox_account(
        #     account_id=sandbox_account.account_id
        # )
        # print(sandbox_account)


if __name__ == "__main__":
    main()
