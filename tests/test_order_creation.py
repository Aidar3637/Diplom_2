import requests
import allure
import uuid

def generate_unique_user():
    """Генерация уникальных данных для пользователя."""
    email = f"{uuid.uuid4()}@example.com"
    password = "password123"
    name = "Generated User"
    return email, password, name
@allure.suite("Тесты создания заказа")
class TestOrderCreation:
    @allure.title("1.Создание заказа с авторизацией")
    @allure.description("Тест проверяет успешное создание заказа авторизованным пользователем.")
    def test_create_order_with_auth(self, base_url, create_user, login_user, get_ingredient_ids):
        """Создание заказа с авторизацией."""
        email, password, name = generate_unique_user()
        create_response = create_user(email, password, name)
        create_response.raise_for_status()

        login_response = login_user(email, password)
        login_response.raise_for_status()
        access_token = login_response.json().get("accessToken")
        assert access_token, f"Токен авторизации не получен: {login_response.text}"

        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        ingredient_ids = get_ingredient_ids()
        payload = {"ingredients": ingredient_ids[:2]}

        with allure.step("Отправка запроса на создание заказа с авторизацией"):
            response = requests.post(f"{base_url}/orders", json=payload, headers=headers)
            response.raise_for_status()
        with allure.step("Проверка ответа"):
            response_json = response.json()
            assert response_json.get("success"), "Заказ не создан"
            assert "order" in response_json, "Поле 'order' отсутствует в ответе"
            assert "_id" in response_json["order"], "ID заказа не получен"
    @allure.title("2.Создание заказа без авторизации")
    @allure.description("Тест проверяет создание заказа без авторизации, с указанными ингредиентами.")
    def test_create_order_without_auth(self, base_url, get_ingredient_ids):
        """Создание заказа без авторизации."""
        ingredient_ids = get_ingredient_ids()
        payload = {"ingredients": ingredient_ids[:2]}

        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = requests.post(f"{base_url}/orders", json=payload)
            response.raise_for_status()
        with allure.step("Проверка ответа"):
            response_json = response.json()
            assert response_json.get("success"), "Заказ не создан"
            assert "order" in response_json, "Поле 'order' отсутствует в ответе"
            assert "number" in response_json["order"], "Номер заказа не получен"
    @allure.title("3.Создание заказа с ингредиентами")
    @allure.description("Тест проверяет возможность создания заказа с несколькими указанными ингредиентами.")
    def test_create_order_with_ingredients(self, base_url, get_ingredient_ids):
        """Создание заказа с ингредиентами."""
        ingredient_ids = get_ingredient_ids()
        payload = {"ingredients": ingredient_ids[:3]}

        with allure.step("Отправка запроса на создание заказа с ингредиентами"):
            response = requests.post(f"{base_url}/orders", json=payload)
            response.raise_for_status()
        with allure.step("Проверка ответа"):
            response_json = response.json()
            assert response_json.get("success"), "Заказ не создан"
            assert "order" in response_json, "Поле 'order' отсутствует в ответе"
            assert "number" in response_json["order"], "Номер заказа не получен"
    @allure.title("4.Создание заказа без ингредиентов")
    @allure.description("Тест проверяет обработку ошибки при создании заказа без указания ингредиентов.")
    def test_create_order_without_ingredients(self, base_url):
        """Создание заказа без ингредиентов."""
        payload = {"ingredients": []}

        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = requests.post(f"{base_url}/orders", json=payload)
        with allure.step("Проверка ответа"):
            assert response.status_code == 400, f"Ожидалась ошибка: {response.text}"
            response_json = response.json()
            assert not response_json.get("success"), "Ожидалось значение success = False"
            assert response_json.get("message") == "Ingredient ids must be provided", "Неверное сообщение об ошибке"
    @allure.title("5.Создание заказа с неверным хешем ингредиентов")
    @allure.description("Тест проверяет создание заказа с неверным идентификатором ингредиентов и обработку ошибки.")
    def test_create_order_with_invalid_ingredient_hash(self, base_url):
        """Создание заказа с неверным хешем ингредиентов."""
        payload = {"ingredients": ["invalid_hash"]}

        with allure.step("Отправка запроса на создание заказа с неверным хешем ингредиентов"):
            response = requests.post(f"{base_url}/orders", json=payload)
        with allure.step("Проверка ответа"):
            assert response.status_code == 400, f"Ожидалась ошибка: {response.text}"
            response_json = response.json()
            assert not response_json.get("success"), "Ожидалось значение success = False"
            assert response_json.get("message") == "One or more ids provided are incorrect", "Неверное сообщение об ошибке"
