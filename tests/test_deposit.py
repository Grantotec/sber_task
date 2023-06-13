from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_bad_input_data_date():
    response = client.post(
        '/api/v1/deposit',
        json={
            "date": "",
            "periods": "3",
            "amount": "10000",
            "rate": "6"
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "date string does not match regex \"\\d{2}.\\d{2}.\\d{4}\""
    }


def test_bad_input_data_periods():
    response = client.post(
        '/api/v1/deposit',
        json={
            "date": "31.01.2021",
            "periods": "",
            "amount": "10000",
            "rate": "6"
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "periods value is not a valid integer"
    }


def test_bad_input_data_amount():
    response = client.post(
        '/api/v1/deposit',
        json={
            "date": "31.01.2021",
            "periods": "3",
            "amount": "",
            "rate": "6"
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "amount value is not a valid integer"
    }


def test_bad_input_data_rate():
    response = client.post(
        '/api/v1/deposit',
        json={
            "date": "31.01.2021",
            "periods": "3",
            "amount": "10000",
            "rate": ""
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "rate value is not a valid float"
    }


def test_good_request():
    response = client.post(
        '/api/v1/deposit',
        json={
            "date": "31.01.2021",
            "periods": "3",
            "amount": "10000",
            "rate": "6"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "31.01.2021": 10050,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75
    }
