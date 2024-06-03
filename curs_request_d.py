import requests
import datetime


def request_curs(pdate, date_curs):  # Функция по дате получает курсы валют и выводит на экран.
    try:
        # Делаем запрос. Параметры periodicity=0 - ежедневный курс, ondate=pdate (дата курсов, вводится в программе)
        # res - ответ
        res = requests.get("https://api.nbrb.by/exrates/rates", params={"periodicity": 0, "ondate": pdate})
        date = res.json()
        if date:  # Данные есть
            # Преобразовываем res в список типа
            # [
            #    {
            #        "Cur_ID": 507,
            #        "Date": "2023-01-10T00:00:00",
            #        "Cur_Abbreviation": "AZN",
            #        "Cur_Scale": 1,
            #        "Cur_Name": "Азербайджанский манат",
            #        "Cur_OfficialRate": 1.6096
            #    },
            # ....
            # ]
            # В цикле перебираем элементы списка. Каждый элемент помещаем в curs
            for curs in date:
                # Преобразовываем дату типа 2023-01-10T00:00:00 в 01.10.202
                # Выводим результат, типа
                # Код валюты: 459, Дата: 2024.06.01, Код: KZT, Курс: 7.2022 за 1000 Тенге
                if curs['Cur_Abbreviation'] != 'USD' and curs['Cur_Abbreviation'] != 'EUR' and curs[
                    'Cur_Abbreviation'] != 'RUB':
                    print(
                        f"Код валюты: {curs['Cur_ID']}, Курс: {curs['Cur_OfficialRate']} за {curs['Cur_Scale']} {curs['Cur_Name']}")
        else:  # Данных нет
            print(f"Нет данных за {date_curs}!")
    except Exception as e:
        print("Ошибка :", e)


def request_curs_val(pdate, date_curs, val):
    try:
        res = requests.get(f"https://api.nbrb.by/exrates/rates/{val}",
                           params={"periodicity": 0, "ondate": pdate, "parammode": 2})
    except Exception as e:
        print("Ошибка :", e)
    else:
        date = res.json()
        if 'status' in date: # Если есть status
            if date['status'] == 404:  # и его значение 404,
                date = "" # то это означает, что нет данных.
        if date:  # Данные есть
            print(
                f"Код валюты: {date['Cur_ID']}, Курс: {date['Cur_OfficialRate']} за {date['Cur_Scale']} {date['Cur_Name']}")
        else:  # Данных нет
            print(f"Нет данных по валюте {val} за {date_curs}!")


date_curs = input("Введите дату в виде ДД.ММ.ГГГГ: ")
try:
    # Преобразовываем дату ДД.ММ.ГГГГ в ГГГГ-ММ-ДД
    formatted_date = datetime.datetime.strptime(date_curs, '%d.%m.%Y').strftime('%Y-%m-%d')
    # если дата задана верно, выполняем запрос
except:
    # Если дата задана неверно, выводим сообщение об ошибке
    print("Дата задана неверно!")
else:
    print(f"Дата курсов: {date_curs}")
    print('Основные валюты')
    request_curs_val(formatted_date, date_curs, 'USD')
    request_curs_val(formatted_date, date_curs, 'EUR')
    request_curs_val(formatted_date, date_curs, 'RUB')
    print('Прочие валюты')
    request_curs(formatted_date, date_curs)
input("Нажмите Enter")
