import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@pytest.fixture
def base_url():
    """Возвращает базовый URL для API."""
    return BASE_URL

@pytest.fixture
def create_user():
    """Фикстура для создания нового пользователя и его удаления после теста."""
    users = []

    def _create_user(email, password, name):
        payload = {"email": email, "password": password, "name": name}
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 200:
            users.append((email, password))
        return response

    yield _create_user

    # Удаление созданных пользователей после теста
    for email, password in users:
        # Авторизация для получения access_token
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        if login_response.status_code == 200:
            access_token = login_response.json().get("accessToken")
            headers = {"Authorization": access_token}
            # Удаление пользователя
            delete_response = requests.delete(f"{BASE_URL}/auth/user", headers=headers)
            if delete_response.status_code != 202:
                print(f"Не удалось удалить пользователя {email}: {delete_response.text}")
        else:
            print(f"Не удалось авторизоваться для удаления пользователя {email}: {login_response.text}")

    users.clear()

@pytest.fixture
def login_user():
    """Фикстура для авторизации пользователя."""
    def _login_user(email, password):
        payload = {"email": email, "password": password}
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        return response
    return _login_user

@pytest.fixture
def create_order():
    """Фикстура для создания нового заказа."""
    def _create_order(access_token, ingredients):
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
        payload = {"ingredients": ingredients}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)
        return response
    return _create_order

@pytest.fixture
def get_ingredient_ids():
    """Фикстура для получения списка ID ингредиентов."""
    def _get_ingredient_ids():
        response = requests.get(f"{BASE_URL}/ingredients")
        response.raise_for_status()
        data = response.json()
        return [item["_id"] for item in data["data"]]
    return _get_ingredient_ids

def pytest_collection_modifyitems(items):
    """
    Переопределяет название классов в отчете Allure:
    - Заменяет "TestOrderCreation" на "Создание заказа".
    - Заменяет "TestOrderRetrievalUser" на "Получение заказов конкретного пользователя".
    - Заменяет "TestUserCreation" на "Создание пользователя".
    - Заменяет "TestUserLogin" на "Логин пользователя".
    - Заменяет "TestUserUpdate" на "Изменение данных пользователя".
    """
    for item in items:
        if "TestOrderCreation" in item.nodeid:
            item._nodeid = item.nodeid.replace("TestOrderCreation", "Создание заказа")
        elif "TestOrderRetrievalUser" in item.nodeid:
            item._nodeid = item.nodeid.replace("TestOrderRetrievalUser", "Получение заказов конкретного пользователя")
        elif "TestUserCreation" in item.nodeid:
            item._nodeid = item.nodeid.replace("TestUserCreation", "Создание пользователя")
        elif "TestUserLogin" in item.nodeid:
            item._nodeid = item.nodeid.replace("TestUserLogin", "Логин пользователя")
        elif "TestUserUpdate" in item.nodeid:
            item._nodeid = item.nodeid.replace("TestUserUpdate", "Изменение данных пользователя")
