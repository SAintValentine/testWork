import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

data = pd.read_csv('Test_4.csv', ";")

def fD(row): # смотрели на общее поведение пользователей по дням
    return row['time_stamp'][:2]


data['day'] = data.apply(fD, axis=1)
data.pivot_table( 'sender_id', 'day', 'gender', 'count').plot(kind='bar', stacked=True,
                                                   title='A/B Test Bar Graph')
plt.show()
del data['day']


def fV(row): # добавляем столбец, отвечающий за версию (basic / test)
    if row['sender_id'] % 2 == 0:
        val = 'basic'
    else:
        val = 'test'
    return val


data['version'] = data.apply(fV, axis=1)
data['datetime'] = pd.to_datetime(data['time_stamp'])

mask = (data['datetime'] > '2017-3-24') & (data['datetime'] < '2017-3-27') # создаем маски
                            # для получения данных за нужный период (когда налчали a/b тестирование)
                            # важно заметить, что отбрасывается дата и за 27 число, ведь там всего 1 клик, что
                            # не является показательным
mask2 = data['datetime'] < '2017-3-25'
mask3 = data['datetime'] > '2017-3-25'

data = data.loc[mask] # уже непосредственно отбрасываем данные
data24 = data.loc[mask2]
data = data.loc[mask3]

start = dt.time(16, 0) # отбрасываем лишнее время за 24.03.2017 (время до 16:00)
end = dt.time(23, 59)
data24 = data24.set_index(['datetime'])
data24 = data24.loc[start:end]

data = pd.concat([data.reset_index(drop=True), data24.reset_index(drop=True)]) # так как было разделено 24 и 25-26 числа
                                                # то сейчас нужно их соеденить обратно, чтобы получить уже итоговый
                                                # промежуток теста
del data['datetime']


def fD(row): # функция для создания поля "День", чтобы не замусоривать графики
    return row['time_stamp'][:2]


data['day'] = data.apply(fD, axis=1)

fig, axes = plt.subplots(ncols=2) # выводим нужные графики
data.pivot_table('sender_id', 'day', 'version', 'count').plot(ax=axes[0],
                                                              kind='bar', stacked=False,
                                                              title='A/B Test Bar Graph')
data.pivot_table('sender_id', 'day', 'version', 'count').plot(ax=axes[1],
                                                              title='A/B Test Graph')
plt.show()

fig, axes = plt.subplots(ncols=2)
data.pivot_table('sender_id', 'gender', 'version', 'count').plot(ax=axes[0],
                                                                 kind='bar', stacked=False,
                                                                 title='A/B Test Gender Bar Graph')
data.pivot_table('sender_id', 'platform_id', 'version', 'count').plot(ax=axes[1],
                                                                      kind='bar', stacked=False,
                                                                      title='A/B Test Platform Bar Graph')

data.pivot_table('sender_id', 'reg_date', 'version', 'count').plot(title='A/B Test Reg.Day Bar Graph')

maskGenderF = data['gender'] == "m" # посмотрим поведение пользователей, обьедененных платформой и гендером
maskGenderM = data['gender'] == "f"
dataM = data.loc[maskGenderM]
dataF = data.loc[maskGenderF]

fig, axes = plt.subplots(ncols=2)
dataM.pivot_table('sender_id', 'platform_id', 'version', 'count').plot(ax=axes[0], kind='bar', stacked=False,
                                                                   title='A/B Test GenderM&Platform Bar')
dataF.pivot_table('sender_id', 'platform_id', 'version', 'count').plot(ax=axes[1], kind='bar', stacked=False,
                                                                   title='A/B Test GenderF&Platform Bar')

plt.show()
# print(data) # для вывода всех данных

numBasic = 0 # подсчет результатов по группам
numTest = 0
for index, row in data.iterrows():
    if row['version'] == "basic":
        numBasic += 1
    else:
        numTest += 1
print("На ", numBasic / numTest * 100 - 100, "% по количеству лайков базовый вариант лучше тестового.") # выведено сравнение по лайкам, остальные
                                                                        # данные будут отображены и обьяснены графиками как просилось в задании


