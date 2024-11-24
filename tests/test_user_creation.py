import requests
import allure
import uuid

def generate_unique_email():
    """Генерация уникального email для пользователя."""
    return f"{uuid.uuid4()}@example.com"
@allure.suite("Тесты создание пользователя")
class TestUserCreation:
    @allure.title("1. Создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание уникального пользователя.")
    def test_create_unique_user(self, create_user, base_url):
        """Создание уникального пользователя."""
        unique_email = generate_unique_email()
        password = "password123"
        name = "Unique User"
        response = create_user(unique_email, password, name)
        with allure.step("Проверка ответа"):
            assert response.status_code == 200, f"Уникальный пользователь не создан: {response.json()}"
            assert "accessToken" in response.json(), "Токен не возвращён"
    @allure.title("2. Создание уже существующего пользователя")
    @allure.description("Тест проверяет ошибку при создании пользователя, который уже зарегистрирован.")
    def test_create_existing_user(self, create_user, base_url):
        """Создание пользователя, который уже зарегистрирован."""
        email = generate_unique_email()  # Генерация уникального email
        password = "password123"
        name = "Existing User"
        create_user(email, password, name)  # Создаём пользователя через фикстуру
        payload = {"email": email, "password": password, "name": name}
        with allure.step("Отправка запроса на создание уже существующего пользователя"):
            response = requests.post(f"{base_url}/auth/register", json=payload)
        with allure.step("Проверка ответа"):
            assert response.status_code == 403, f"Ожидалась ошибка при создании существующего пользователя: {response.json()}"
            assert response.json()["message"] == "User already exists", "Неверное сообщение об ошибке"
    @allure.title("3. Создание пользователя без обязательного поля")
    @allure.description("Тест проверяет ошибку при создании пользователя без обязательного поля.")
    def test_create_user_missing_field(self, base_url):
        """Создание пользователя без одного из обязательных полей."""
        payload = {"email": generate_unique_email(), "password": "password123"}  # Пропущено обязательное поле name
        with allure.step("Отправка запроса на создание пользователя без обязательного поля"):
            response = requests.post(f"{base_url}/auth/register", json=payload)
        with allure.step("Проверка ответа"):
            assert response.status_code == 403, f"Ожидалась ошибка при отсутствии обязательного поля: {response.json()}"
            assert response.json()["message"] == "Email, password and name are required fields", "Неверное сообщение об ошибке"
