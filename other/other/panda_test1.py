import pandas as pd
from pandas import DataFrame

d1 = {

    "Стобец 1": 2000,
    "Столбец 2": "Треугольник"

}

d2 = {

    "Стобец 1": 3000,
    "Столбец 2": "Квадрат"

}


df = pd.DataFrame([d1, d2])

print(df)