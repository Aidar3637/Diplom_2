import requests
import allure
import uuid

def generate_unique_user():
    """Генерация уникальных данных для пользователя."""
    email = f"{uuid.uuid4()}@example.com"
    password = "password123"
    name = "Generated User"
    return email, password, name
@allure.suite("Тесты изменения данных пользователя")
class TestUserUpdate:
    @allure.title("1. Изменение данных пользователя с авторизацией")
    @allure.description("Тест проверяет успешное изменение данных пользователя с использованием токена авторизации.")
    def test_update_user_with_auth(self, base_url, create_user, login_user):
        """Изменение данных пользователя с авторизацией."""
        email, password, name = generate_unique_user()  # Генерация данных пользователя

        # Создание пользователя
        create_response = create_user(email, password, name)
        assert create_response.status_code == 200, f"Ошибка при создании пользователя: {create_response.json()}"

        # Логин пользователя
        login_response = login_user(email, password)
        assert login_response.status_code == 200, f"Ошибка при логине: {login_response.json()}"
        access_token = login_response.json().get("accessToken")
        assert access_token, f"Токен авторизации не получен: {login_response.json()}"

        # Изменение данных пользователя
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
        payload = {"name": "Updated Name"}
        with allure.step("Отправка запроса на изменение данных пользователя с авторизацией"):
            response = requests.patch(f"{base_url}/auth/user", json=payload, headers=headers)
        with allure.step("Проверка ответа"):
            assert response.status_code == 200, f"Ошибка при обновлении данных: {response.json()}"
            assert response.json()["user"]["name"] == "Updated Name", "Имя пользователя не обновлено"
    @allure.title("2. Изменение данных пользователя без авторизации")
    @allure.description("Тест проверяет ошибку при попытке изменить данные пользователя без авторизации.")
    def test_update_user_without_auth(self, base_url):
        """Изменение данных пользователя без авторизации."""
        payload = {"name": "Updated Name"}
        with allure.step("Отправка запроса на изменение данных пользователя без авторизации"):
            response = requests.patch(f"{base_url}/auth/user", json=payload)
        with allure.step("Проверка ответа"):
            assert response.status_code == 401, f"Ожидалась ошибка авторизации: {response.json()}"
            assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"
