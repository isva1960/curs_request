import requests
import datetime


def request_curs(pdate):  # Функция по дате получает курсы валют и выводит на экран.
    try:
        # Делаем запрос. Параметры periodicity=0 - ежедневный курс, ondate=pdate (дата курсов, вводится в программе)
        # res - ответ
        res = requests.get("https://api.nbrb.by/exrates/rates", params={"periodicity": 0, "ondate": pdate})
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
        date = res.json()
        if date:  # Данные есть
            # В цикле перебираем элементы списка. Каждый элемент помещаем в curs
            for curs in date:
                # Преобразовываем дату типа 2023-01-10T00:00:00 в 01.10.202
                date = datetime.datetime.strptime(curs['Date'], '%Y-%m-%dT%H:%M:%S').strftime("%Y.%m.%d")
                # Выводим результат, типа
                # Код валюты: 459, Дата: 2024.06.01, Код: KZT, Курс: 7.2022 за 1000 Тенге
                print(
                    f"Код валюты: {curs['Cur_ID']}, Дата: {date}, Код: {curs['Cur_Abbreviation']}, Курс: {curs['Cur_OfficialRate']} за {curs['Cur_Scale']} {curs['Cur_Name']}")
        else:  # Данных нет
            print("Нет данных!")
    except Exception as e:
        print("Ошибка :", e)


date_curs = input("Введите дату в виде ДД.ММ.ГГГГ: ")
try:
    # Преобразовываем дату ДД.ММ.ГГГГ в ГГГГ-ММ-ДД
    formatted_date = datetime.datetime.strptime(date_curs, '%d.%m.%Y').strftime('%Y-%m-%d')
    # если дата задана верно, выполняем запрос
    request_curs(formatted_date)
except:
    # Если дата задана неверно, выводим сообщение об ошибке
    print("Дата задана неверно!")
input("Нажмите Enter")
