# import bot_trading.lib.tinkoff.tinkoff_main as tinkoffmain
import bot_trading.lib.db.db_main as dbmain

def db_update_cell(table, ticker, column, value):
    with dbmain.Session(autoflush=False, bind=dbmain.engine) as db:
        qs_num_one = db.query(table).filter(table.ticker == ticker).first()
        setattr(qs_num_one, column, value)
        # print("Обновил пасс ризон")
        db.commit()

def db_update_cell_by_id(table, id, column, value):
    with dbmain.Session(autoflush=False, bind=dbmain.engine) as db:
        qs_num_one = db.query(table).filter(table.id == id).first()
        setattr(qs_num_one, column, value)
        # print("Обновил пасс ризон")
        db.commit()
def db_insert_log(data):
    with dbmain.Session(autoflush=False, bind=dbmain.engine) as db:
        tom = dbmain.Log1(**data)
        db.add(tom)  # добавляем в бд
        db.commit()  # сохраняем изменения