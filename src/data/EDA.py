# Импортируем библиотеки

import pandas as pd
from pathlib import Path
import warnings
import os


# from setup import basedir


warnings.filterwarnings("ignore")

# PATH =
# basedir = setup.basedir
# basedir = os.path.abspath(os.path.dirname(__file__))
BASEDIR = Path(__file__).parent.parent.parent
# basedir = os.path.abspath(os.path.dirname(__file__))
print(BASEDIR)

DATA_FILE = os.path.join(BASEDIR, "data/raw")
print(DATA_FILE)


# Смотрим на первый файл
df_1 = pd.read_csv(
    os.path.join(DATA_FILE, "data_csv.csv"), sep=";", encoding="windows-1251"
)
print(df_1)
df_1.info()

# Смотрим на второй файл
df_2 = pd.read_csv(
    os.path.join(DATA_FILE, "data2.csv"), sep=";", encoding="windows-1251"
)
print(df_2)
df_2.info()

# Смотрим на третий файл
df_3 = pd.read_csv(
    os.path.join(DATA_FILE, "kniga_data.csv"), sep=";", encoding="windows-1251"
)
print(df_3)
df_3.info()

# Видимо эти файлы кто-то пытался сделать из другого, они не совсем полные. Посмотрим на книгу ексель
xls = pd.ExcelFile(os.path.join(DATA_FILE, "Kniga1.xlsx"))
df1 = pd.read_excel(xls, "Остеопороз лаб")
print(df1)
df1.info()

df2 = pd.read_excel(xls, "Остео сопут")
print(df2)
df2.info()

# Переименуем столбец, т.к. там закрылся лишний пробел
df2 = df2.rename({" Ф.И.О.": "Ф.И.О."}, axis="columns")
df2.info()

df3 = pd.read_excel(xls, "Остео жалобы")
print(df3)
df3.info()

# Смержим посмотренные листы, т.к. там клиника на одних и тех же людей
df1_1 = df1.merge(df2, on="Ф.И.О.")
df1_2 = df1_1.merge(df3, on="Ф.И.О.")
df1_2.info()
print(df1_2)

df4 = pd.read_excel(xls, "Остео_перелом")
print(df4)
df4.info()

df5 = pd.read_excel(xls, "СД_прочие")
print(df5)
df5.info()

# Переименуем столбец, т.к. там закрылся лишний пробел
df5 = df5.rename({" Ф.И.О.": "Ф.И.О."}, axis="columns")

df6 = pd.read_excel(xls, "СД_остео_жалобы")
print(df6)
df6.info()

# Смержим данные листы, т.к. тут клиника на одних и тех же людей
df2_1 = df4.merge(df5, on="Ф.И.О.")
df2_1.info()

# Смержим данные листы, т.к. тут клиника на одних и тех же людей
df2_2 = df2_1.merge(df6, on="Ф.И.О.")
df2_2.info()
print(df2_2)

# Видимо из-за неполного заполнения данных в таблице добавились данные, неперсоанализированного характера, убьем их
df2_2 = df2_2[:52]
df2_2.info()


DATA_INTERIM = os.path.join(BASEDIR, "data/interim")


df1_2.to_csv(os.path.join(DATA_INTERIM, "df1_2.csv"))
df2_2.to_csv(os.path.join(DATA_INTERIM, "df2_2.csv"))
