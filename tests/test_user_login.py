import requests
import allure

@allure.suite("Тесты логина пользователя")
class TestUserLogin:
    @allure.title("1. Логин существующего пользователя")
    @allure.description("Тест проверяет успешный логин зарегистрированного пользователя.")
    def test_login_existing_user(self, base_url, create_user):
        """Логин существующего пользователя."""
        email = "existing_user@example.com"
        password = "password123"
        name = "Existing User"
        create_user(email, password, name)  # Создаём пользователя через фикстуру

        payload = {"email": email, "password": password}
        with allure.step("Отправка запроса на логин существующего пользователя"):
            response = requests.post(f"{base_url}/auth/login", json=payload)
        with allure.step("Проверка ответа"):
            assert response.status_code == 200, f"Ошибка при логине: {response.json()}"
            assert "accessToken" in response.json(), "Токен не возвращён"
    @allure.title("2. Логин с неверным логином или паролем")
    @allure.description("Тест проверяет ошибку при попытке логина с неверным логином или паролем.")
    def test_login_invalid_credentials(self, base_url):
        """Логин с неверным логином или паролем."""
        payload = {"email": "wrong_user@example.com", "password": "wrong_password"}
        with allure.step("Отправка запроса на логин с неверным логином или паролем"):
            response = requests.post(f"{base_url}/auth/login", json=payload)
        with allure.step("Проверка ответа"):
            assert response.status_code == 401, f"Ожидалась ошибка при неверных данных: {response.json()}"
            assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"
