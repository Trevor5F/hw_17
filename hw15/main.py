import sqlite3
from constants import OLD_DATABASE, CREATE_QUERIES, MIGRATE_SECOND, MIGRATE_JOIN
from flask import Flask, jsonify
import logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

app = Flask(__name__)


def get_sqlite_query(query, base=OLD_DATABASE, is_script=False):
    """Читаем старую базу данных"""
    with sqlite3.connect(base) as connection:
        cursor = connection.cursor()
        if is_script:
            result = cursor.executescript(query)
        else:
            result = cursor.execute(query)
        return result.fetchall()


def get_all_by_id(id):
    query = f"""
    SELECT * 
    FROM animals_new
    WHERE id == {id}
    """

    raw = get_sqlite_query(query, is_script=False)
    result_dict = {'id': raw[0][0], 'age_upon_outcome': raw[0][1], 'animal_id': raw[0][2],
                   'name': raw[0][3], 'id_type': raw[0][4], 'id_breed': raw[0][5],
                   'id_color1': raw[0][6], 'id_color2': raw[0][7], 'dateOfBirth': raw[0][8][0:10],
                   'id_outcome_subtype': raw[0][9], 'id_outcome_type': raw[0][10], 'outcome_month': raw[0][11],
                   'outcome_year': raw[0][12]}
    return result_dict


# Создание новых таблиц. Основная таблица + допы
get_sqlite_query(CREATE_QUERIES, is_script=True)

# Заполнение доп. таблиц данными
get_sqlite_query(MIGRATE_SECOND, is_script=True)

# Заполнение основной таблицы айдишниками через JOIN
get_sqlite_query(MIGRATE_JOIN, is_script=False)

# print((get_all_by_id(1)))

@app.route('/<id>/')
def get_by_id(id):
    """ Шаг 1. Поиск по названию самого свежего """
    logging.info(f'Ищем по ID: {id}')

    animal = get_all_by_id(id)  # Словарь с данными по ОДНОМУ посту
    logging.info(f'Функция поиска вернула: {animal}')

    return jsonify(animal)

app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(debug=True)
