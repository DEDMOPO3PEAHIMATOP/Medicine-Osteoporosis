# Импортируем библиотеки

import os
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")

BASEDIR = Path(__file__).parent.parent.parent

DATA_INTERIM = os.path.join(BASEDIR, 'data/interim')

df1_2 = pd.read_csv(os.path.join(DATA_INTERIM, 'df1_2.csv'))
df2_2 = pd.read_csv(os.path.join(DATA_INTERIM, 'df2_2.csv'))

# Видимо из-за неполного заполнения данных в таблице добавились данные, неперсоанализированного характера, убьем их
df2_2 = df2_2[:52]
df2_2.info()

# Выделим колонки со схожими наименованиями
columns_1 = list(df1_2.columns.values)
columns_2 = list(df2_2.columns.values)
column12 = []
for col in columns_1:
    if col in columns_2:
        print(col, 'Есть в обоих базах')
        column12.append(col)
    else:
        print(col, 'Нет во второй базе')

print(column12)

# Сделаем общую базу
df1_2_1 = df1_2[column12]
df2_2_1 = df2_2[column12]
df_merged = df1_2_1._append(df2_2_1, ignore_index=True)

print(df_merged)
df_merged.info()

# Избавимся от года рождения оставив только число полных лет
df_merged['год рождения (возраст)'] = df_merged['год рождения (возраст)'].apply(
    lambda x: float(x.split()[1][1:-1])
    if type(x) is str else float(x))

# Преобразуем в float данные в столбце 'о/хондроз'
df_merged['о/хондроз'] = df_merged['о/хондроз'].apply(
    lambda x: float(1)
    if x == '+' else float(x))
df_merged['о/хондроз'].fillna(0, inplace=True)

# Преобразуем в float данные в столбце 'ЭКГ (Нарушение реполяризации)'
df_merged['ЭКГ (Нарушение реполяризации)'] = df_merged['ЭКГ (Нарушение реполяризации)'].apply(
    lambda x: float(1)
    if x == '+' else float(x))
df_merged['ЭКГ (Нарушение реполяризации)'].fillna(0, inplace=True)

# Преобразуем в float данные в столбце 'син. Тахикардия'
df_merged['син. Тахикардия'] = df_merged['син. Тахикардия'].apply(
    lambda x: float(1)
    if x == '+' else float(x))
df_merged['син. Тахикардия'].fillna(0, inplace=True)

# Преобразуем в float данные в столбце 'ПИКС'
df_merged['ПИКС'] = df_merged['ПИКС'].apply(
    lambda x: float(1)
    if x == '+' else float(x))
df_merged['ПИКС'].fillna(0, inplace=True)

# Преобразуем в float данные в столбце 'ХСН'
df_merged['ХСН'] = df_merged['ХСН'].apply(
    lambda x: float(1)
    if x == 'II' else float(x))
df_merged['ХСН'].fillna(0, inplace=True)

# Преобразуем в float данные в столбце 'ЯБ'
df_merged['ЯБ'] = df_merged['ЯБ'].astype('float')

# Удалим столбцы '№ п/п_x', '№ п/п_y', 'Ф.И.О.' как неинформативные
df_merged = df_merged.drop(['Unnamed: 0', '№ п/п_x', '№ п/п_y', 'Ф.И.О.'], axis=1)

# Заменим пропущенные значения в столбцах 'общий белок, г/л', 'ТТГ', 'ИМТ' и 'ГБ' на средние
df_merged['общий белок, г/л'].fillna((df_merged['общий белок, г/л'].mean()), inplace=True)
df_merged['ГБ'].fillna((df_merged['ГБ'].mean()), inplace=True)
df_merged['ТТГ'].fillna((df_merged['ТТГ'].mean()), inplace=True)
df_merged['ИМТ'].fillna((df_merged['ИМТ'].mean()), inplace=True)

# В итоге получаем
df_merged.info()

DATA_PROCESSED = os.path.join(BASEDIR, 'data/processed')

df_merged.to_csv(os.path.join(DATA_PROCESSED, 'df_merged.csv'))
