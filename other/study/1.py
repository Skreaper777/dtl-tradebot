import datetime
import os

# from tinkoff.invest import Client
from tinkoff.invest.sandbox.client import SandboxClient

# TOKEN = os.environ["INVEST_TOKEN"]
TOKEN = "t.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg"

def main():
    with SandboxClient(TOKEN) as client:
        print(client.users.get_accounts())

        sandbox_accounts = client.sandbox.get_sandbox_accounts()
        # print("Вот все счета в песочнице", sandbox_accounts)

        account_id = sandbox_accounts.accounts[0].id

        r = client.operations.get_operations(
            account_id = account_id,
            from_= datetime.datetime(2021,1,1),
            to = datetime.datetime.now()

        )

        print(r)

if __name__ == "__main__":
    main()