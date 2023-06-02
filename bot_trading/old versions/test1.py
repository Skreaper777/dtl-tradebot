import datetime

from tinkoff.invest import Client

TOKEN = 't.zSv0PvqY9KLK07vFsbvdjHAW0fh-qeN4TXr6PksjPJDUVdIkIFI0RZ-hhHHC2gMY7RHpDxnEcJlnWWmMQZztGg'

with Client(TOKEN) as client:
    acc = client.users.get_accounts()
    # print(client.users.get_accounts())
    print(acc)
    r = client.operations.get_operations(
        account_id='2139991463',
        # account_id=TOKEN.account_id_main,
        from_= datetime.datetime(2022,1,1),
        to = datetime.datetime.now()
    )
    print(r)



