1. Скачать этот репозиторий вручную или клонировать через гит:
   git clone https://github.com/rakhat617/task_manager_drf
2. Зайти через терминал в корень скачанного проекта и активировать виртуальное окружение:
   python -m venv env
   
   source env/bin/activate   # для Linux/Mac
   env\Scripts\activate      # для Windows
3. Установить зависимости:
   pip install -r requirements.txt
4. Создать .env файл в корне проекта и прописать туда ваш секретный ключ (придумайте сами).
   Пропишите эту строчку в .env файле:
   SECRET_KEY="Здесь напишите ваш секретный ключ"
5. Применить миграции. В терминале с активированным окружением в корне проекта пропишите эти строчки:
   python manage.py makemigrations
   python manage.py migrate
6. Создать суперпользователя (опционально):
   python manage.py createsuperuser
7. Запустить сервер разработки:
   python manage.py runserver

note: если у вас не работают команда python, попробуйте py или python3
