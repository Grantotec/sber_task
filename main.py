from fastapi import FastAPI
from datetime import datetime, date, timedelta

app = FastAPI()


@app.get("/")
async def read_item(start_date: str = None,
                    periods: int = None,
                    amount: int = None,
                    rate: float = None
                    ):
    # TODO Валдация

    print(start_date, periods, amount, rate)


    result = {}
    start_date = datetime.strptime(start_date, '%d.%m.%Y')
    next_month = start_date.replace(day=28) + timedelta(days=4)
    last_day_of_month = next_month - timedelta(days=next_month.day)

    while periods > 0:
        date_str = last_day_of_month.strftime('%d.%m.%Y')
        sum = amount * (1 + rate / 12 / 100)
        result[date_str] = round(sum, 2)

        # Обновляем дату последнего дня следующего месяа
        last_day_of_month += timedelta(days=1)
        last_day_of_month = last_day_of_month.replace(day=28) \
                            + timedelta(days=4)
        last_day_of_month = last_day_of_month \
                            - timedelta(days=last_day_of_month.day)
        # Обновляем счетчик периодов
        periods -= 1
        # Обновляем сумму
        amount = sum


    print('Result: ', result)
    return {'Status': 'OK'}
