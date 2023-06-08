from fastapi import FastAPI
from datetime import datetime, date, timedelta

app = FastAPI()


def last_day_of_month(day: date) -> date:
    '''
    Принимает на вход дату и возвращает последний
    день месяца из этой даты
    :param day:
    :return: возвращает последний
    день месяца из этой даты
    '''
    next_month = day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


@app.get("/")
async def read_item(start_date: str = None,
                    periods: int = None,
                    amount: int = None,
                    rate: float = None
                    ):
    # TODO Валдация

    print(start_date, periods, amount, rate)

    output = {}
    start_date = datetime.strptime(start_date, '%d.%m.%Y')

    date_not_str = last_day_of_month(start_date)

    while periods > 0:
        date_str = date_not_str.strftime('%d.%m.%Y')
        summa = amount * (1 + rate / 12 / 100)
        output[date_str] = round(summa, 2)

        # Обновляем дату последнего дня следующего месяа
        next_day = date_not_str + timedelta(days=1)
        date_not_str = last_day_of_month(next_day)

        # Обновляем счетчик периодов
        periods -= 1
        # Обновляем сумму
        amount = summa

    return output, 200
