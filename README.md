# Stellar Burgers API Testing

Описание проекта:
Проект предназначен для автоматизации тестирования API сайта [Stellar Burgers](https://stellarburgers.nomoreparties.site/). Реализованы тесты для проверки основных сценариев взаимодействия с API:

- Создание пользователя
- Логин пользователя
- Изменение данных пользователя
- Создание заказа
- Получение заказов

Используются библиотеки: `pytest`, `requests`, `allure-pytest`.

Структура проекта:
- **tests/** — директория с тестами.
- **locators/** — директория с API эндпоинтами.
- **reports/** — директория для отчётов Allure.
- **requirements.txt** — зависимости проекта.
- **.gitignore** — исключения для Git.
- **README.md** — документация проекта.

Установите зависимости:
   pip3 install -r requirements.txt
  
Запуск тестов:
Для выполнения тестов используйте команду:

pytest --alluredir=reports/allure-results


Генерация отчёта Allure:
1. Убедитесь, что установлен Allure.
2. Сгенерируйте и просмотрите отчёт командой:

   allure serve reports/allure-results



