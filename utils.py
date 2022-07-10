import json
import datetime as dt


# загрузка данных из json файлов
def get_data_from_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# создание обьектов классов из json
def get_objects_list(list, class_):
    objects_list = [class_(**i) for i in list]
    return objects_list


# Преобразование текста в дату
def edit_date_format(data_file):
    for i in data_file:
        i["start_date"] = dt.datetime.strptime(i["start_date"], '%m/%d/%Y')
        i["end_date"] = dt.datetime.strptime(i["end_date"], '%m/%d/%Y')
    return data_file
