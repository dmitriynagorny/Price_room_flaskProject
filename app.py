# Импорт библиотек
from flask import Flask, Markup, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Столбцы таблицы
headers = [
    'Балкон/лоджия',
    'Вид из окон',
    'Время до метро',
    'Всего этажей',
    'Высота потолков',
    'Комнаты',
    'Метро',
    'Окончание стройки',
    'Отделка',
    'Планировка',
    'Площадь',
    'Ремонт',
    'Санузел',
    'Тип жилья',
    'Этаж'
]

# Колонки для энкодера
encoder_columns = [
    'Метро',
    'Вид из окон',
    'Ремонт',
    'Тип жилья',
    'Отделка',
    'Планировка'
]

# Загрузим страницу с параметрами
@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    return render_template('index.html')

# Получим данные
@app.route('/calculation', methods=['POST', 'GET'])
def calculation():
    try:
        balcony = int(request.form['balcony'])
    except Exception:
        balcony = 0
    try:
        room = int(request.form['room'])
    except Exception:
        room = 1
    try:
        floor = int(request.form['floor'])
    except Exception:
        floor = 1
    try:
        floors = int(request.form['floors'])
    except Exception:
        floors = 1
    try:
        height = float(request.form['height'])
    except Exception:
        height = 2.6
    try:
        space = float(request.form['space'])
    except Exception:
        space = room * 25
    try:
        bathroom = int(request.form['bathroom'])
    except Exception:
        bathroom = 1
    try:
        auto_foot = int(request.form['auto_foot'])
    except Exception:
        auto_foot = 1
    try:
        metro_time = int(round(float(request.form['metro_time']))) * auto_foot
    except Exception:
        metro_time = 100
    try:
        years_building = int(request.form['years_building'])
        if years_building < 2022:
            years_building = 0
        elif years_building <= 2023:
            years_building = 1
        else:
            years_building = 2
    except Exception:
        years_building = 0

    metro = request.form['metro']
    repair = request.form['repair']
    finishing = request.form['finishing']
    view_window = request.form['view_window']
    type_house = request.form['type_house']
    plan = request.form['plan']

    cells_list = [balcony, view_window, metro_time, floors, height, room, metro, years_building, finishing, plan, space, repair, bathroom, type_house, floor]
    cells_table = create_table(cells_list)
    html_table = cells_table.to_html()
    predict = prediction(cells_table)
    return render_template('result.html', predict=('{0:,}'.format(int(predict[0])).replace(',', ' ')), table=Markup(html_table))


# Создание таблицы
def create_table(cells):
    table_dict = dict(zip(headers, cells))
    table = pd.DataFrame(table_dict, index=['0'])
    return table


# Загрузка моделей
def save_model():
    encoder_model = pickle.load(open('models/encoder_model.sav', 'rb'))
    cat_model = pickle.load(open('models/finalized_model.sav', 'rb'))
    return encoder_model, cat_model


# Расчет предсказания по моделям
def prediction(data):
    models = save_model()
    data[encoder_columns] = models[0].transform(data[encoder_columns])
    predict = models[1].predict(data)
    return predict


if __name__ == '__main__':
    app.run()
