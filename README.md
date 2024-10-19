
# Car Management Application

Это веб-приложение для управления информацией об автомобилях, разработанное с использованием Django и PostgreSQL. Оно включает в себя функциональность для регистрации пользователей, добавления автомобилей и комментариев.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Ostamer/car_management.git
   cd car_management
2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
Настройте базу данных: Убедитесь, что у вас установлена PostgreSQL и создана база данных с именем CarTest. Измените параметры подключения в файле settings.py, если это необходимо.

## Запуск приложения
1. Примените миграции:

    ```bash
    python manage.py migrate

2. Запустите сервер разработки:

    ```bash
    python manage.py runserver
Теперь вы можете открыть браузер и перейти по адресу http://127.0.0.1:8000/api для доступа к приложению.

## Использование API
1. Регистрация пользователя
1) POST /register/
2) Данные:
3) username: имя пользователя
4) email: email
5) password: пароль
6) password2: подтверждение пароля
2. Аутентификация
1) POST /login/
2) Данные:
3) username: имя пользователя
4) password: пароль
3. Управление автомобилями
1) GET /cars/ - Получить список автомобилей 
2) POST /cars/ - Создать новый автомобиль
3) GET /cars/<int:car_id>/ - Получить информацию об автомобиле
4) PUT /cars/<int:car_id>/ - Обновить информацию об автомобиле
5) DELETE /cars/<int:car_id>/ - Удалить автомобиль
4. Комментарии к автомобилям
1) GET /cars/<int:car_id>/comments/ - Получить список комментариев к автомобилю
2) POST /cars/<int:car_id>/comments/ - Добавить комментарий к автомобилю    