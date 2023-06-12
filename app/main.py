from datetime import datetime, date, timedelta
from pydantic import BaseModel, constr, conint, confloat
from fastapi import FastAPI
from starlette import status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


app = FastAPI()


def last_day_of_month(day: date) -> date:
    """
    Принимает на вход дату и возвращает последний
    день месяца из этой даты
    :param day:
    день месяца из этой даты
    """
    next_month = day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"error": exc.errors()[0]['msg']})
    )


class InputData(BaseModel):
    date: constr(regex=r'\d{2}.\d{2}.\d{4}')
    periods: conint(ge=1, le=60)
    amount: conint(ge=10000, le=3000000)
    rate: confloat(ge=1.0, le=8.0)


@app.post("/api/v1/deposit")
def deposit(input_data: InputData):
    output = {}

    request_date = datetime.strptime(input_data.date, '%d.%m.%Y')

    last_day_of_period = last_day_of_month(request_date)

    # В цикле проходим по всем периодам
    while input_data.periods > 0:
        summa = input_data.amount * (1 + input_data.rate / 12 / 100)
        output[last_day_of_period.strftime('%d.%m.%Y')] = round(summa, 2)

        # Обновляем дату последнего дня следующего месяца
        next_day = last_day_of_period + timedelta(days=1)
        last_day_of_period = last_day_of_month(next_day)

        # Обновляем счетчик периодов
        input_data.periods -= 1
        # Обновляем сумму
        input_data.amount = summa

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output
    )
