import requests
import pytest
from jsonschema.validators import validate

from resources.schemas.login_success import login_success
from resources.schemas.post_user import create_user
from resources.schemas.register_success import register_success
from resources.schemas.update_user import update_user

headers = {'x-api-key': 'reqres-free-v1'}


@pytest.fixture
def url(hand, api) -> str:
    return hand + api


## на каждый из методов GET/POST/PUT/DELETE ручек reqres.in and На разные схемы (4-5 схем)
def test_get_users():
    response = requests.get("https://reqres.in/api/users?pagе=3", headers=headers)

    assert response.status_code == 200


def test_get_single_user():
    response = requests.get("https://reqres.in/api/users/2", headers=headers)

    assert response.status_code == 200


def test_create_user():
    response = requests.post("https://reqres.in/api/users", headers=headers, data={"name": "Andrey", "job": "Driver"})
    body = response.json()
    validate(body, create_user)

    assert body["name"] == "Andrey"
    assert body["job"] == "Driver"
    assert response.status_code == 201


def test_update_user():
    response = requests.put("https://reqres.in/api/users/3", headers=headers, data={"name": "Andrey"})
    body = response.json()
    validate(body, update_user)

    assert body["name"] == "Andrey"
    assert response.status_code == 200


def test_delete_user():
    response = requests.delete("https://reqres.in/api/users/4", headers=headers)

    assert response.status_code == 204


def test_check_register_schema():
    response = requests.post("https://reqres.in/api/register", headers=headers, data={
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
                             )
    body = response.json()

    assert response.status_code == 200
    validate(body, register_success)


def test_check_login_schema():
    response = requests.post("https://reqres.in/api/login", headers=headers, data={
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
                             )
    body = response.json()
    assert response.status_code == 200
    validate(body, login_success)


## Позитивные/Негативные тесты на одну из ручек.

def test_create_user_negative():
    with pytest.raises(Exception):
        response = requests.post("https://reqres.in/api/users", headers=headers, data={"job": "Driver"})
        body = response.json()
        validate(body, create_user)


def test_create_user_positive():
    response = requests.post("https://reqres.in/api/users", headers=headers, data={"name": "Tolik", "job": "Driver"})
    body = response.json()

    assert body["name"] == "Tolik"
    validate(body, create_user)


#На разные статус-коды 204/404/400, 201,200,204 уже есть выше

def test_status_code_400():
    response = requests.post("https://reqres.in/api/register", headers=headers, data={"email": "sydney@fife"})

    assert response.status_code == 400


def test_status_code_404():
    response = requests.get("https://reqres.in/api/unknown/23", headers=headers)

    assert response.status_code == 404


## С ответом и без ответа, тоже реализовано выше
