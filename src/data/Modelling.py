# Импортируем библиотеки

import warnings

import os
import pandas as pd
from pathlib import Path
from sklearn.naive_bayes import GaussianNB
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

BASEDIR = Path(__file__).parent.parent.parent
DATA_PROCESSED = os.path.join(BASEDIR, 'data/processed')
df_merged = pd.read_csv(os.path.join(DATA_PROCESSED, 'df_merged.csv'))

# Выделим наши features и targets
fracture_colls = df_merged.filter(like='перелом').columns
targets = df_merged[['перелом лучевой кости', ' перелом позвоночника (уровень)', ' перелом бедра']]
targets['перелом'] = targets.max(axis=1)
features = df_merged.drop(fracture_colls, axis=1)
print(features)

targets.mean()

# Сделаем предустановки для обучения моделей
n_splits = 7
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=12345)


# Функция подсчета скора для каждого таргета
def clf_scores(clf):
    for col in targets.columns:
        scores = cross_val_score(clf, features, targets[col], cv=skf, scoring='roc_auc')
        print(col, 'all scores', scores.round(2))
        print(' mean ', round(scores.mean(), 3), '\n')


# Предскажем методом Гаусса
clf_scores(GaussianNB())

# Предскажем методом Опорных векторов
clf_scores(SVC(random_state=12345))

# Предскажем методом Деверьев решений
clf_scores(DecisionTreeClassifier(random_state=12345))

# Предскажем Логистической регрессией
clf_scores(LogisticRegression(max_iter=1500, random_state=12345))

# Предскажем методом Ближайший соседей
clf_scores(KNeighborsClassifier())

# Предскажем методом Случайного леса
clf_scores(RandomForestClassifier(random_state=12345))

# Предскажем Какбустом
clf_scores(CatBoostClassifier(logging_level='Silent', random_seed=12345))

# Кактбуст дает нам предсказания в 0,971, а логистическая регрессия в частности предсказание перелома бедра 0,688
# вместо 0,432 катбуста - надо посмотреть как мы будем и что именно предсказывать в будующем
