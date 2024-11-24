import requests
import allure
import uuid

def generate_unique_user():
    """Генерирует уникальные данные пользователя."""
    email = f"{uuid.uuid4()}@example.com"
    password = "password123"
    name = "Generated User"
    return email, password, name
@allure.suite("Тесты получения заказов конкретного пользователя")
class TestOrderRetrievalUser:
    @allure.title("1. Получение заказов авторизованным пользователем")
    @allure.description("Тест проверяет успешное получение заказов авторизованным пользователем.")
    def test_get_orders_with_auth(self, base_url, create_user, login_user):
        """Тест получения заказов с авторизацией."""
        # Генерация и авторизация пользователя
        email, password, name = generate_unique_user()
        create_response = create_user(email, password, name)
        assert create_response.status_code == 200, f"Ошибка при создании пользователя: {create_response.text}"

        login_response = login_user(email, password)
        assert login_response.status_code == 200, f"Ошибка при логине: {login_response.text}"
        access_token = login_response.json().get("accessToken")
        assert access_token, f"Токен авторизации не получен: {login_response.text}"

        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        # Получение списка ингредиентов
        ingredients_response = requests.get(f"{base_url}/ingredients")
        assert ingredients_response.status_code == 200, f"Ошибка при получении ингредиентов: {ingredients_response.text}"
        ingredients_data = ingredients_response.json()
        ingredient_ids = [item["_id"] for item in ingredients_data["data"]]

        # Создание заказа
        payload = {"ingredients": ingredient_ids[:2]}
        order_response = requests.post(f"{base_url}/orders", json=payload, headers=headers)
        assert order_response.status_code == 200, f"Ошибка при создании заказа: {order_response.text}"

        # Получение заказов пользователя
        with allure.step("Получение заказов авторизованного пользователя"):
            response = requests.get(f"{base_url}/orders", headers=headers)
        with allure.step("Проверка ответа"):
            assert response.status_code == 200, f"Ошибка при получении заказов: {response.text}"
            response_json = response.json()
            assert response_json.get("success"), "Поле 'success' отсутствует или False"
            assert "orders" in response_json, "Поле 'orders' отсутствует в ответе"
            assert len(response_json["orders"]) > 0, "Список заказов пуст"
    @allure.title("2. Получение заказов неавторизованным пользователем")
    @allure.description("Тест проверяет ошибку при попытке получения заказов неавторизованным пользователем.")
    def test_get_orders_without_auth(self, base_url):
        """Тест получения заказов без авторизации."""
        # Попытка получить заказы без авторизации
        with allure.step("Попытка получения заказов без авторизации"):
            response = requests.get(f"{base_url}/orders")
        with allure.step("Проверка ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
            response_json = response.json()
            assert not response_json.get("success"), "Ожидалось, что 'success' будет False"
            assert response_json.get("message") == "You should be authorised", "Неверное сообщение об ошибке"
