# 🐍 Проект «WhereToGo — Москва глазами Артёма»

![главная](https://github.com/user-attachments/assets/ec0ef2b0-388f-45d5-aae7-3ab382abed91)

**Проект доступен по ссылке:** [Демо-версия](https://decebell032.pythonanywhere.com)
**Панель администратора:**  [Админка](https://decebell032.pythonanywhere.com/admin)

## 📌 Описание проекта

**WhereToGo** — это веб-приложение на Django, позволяющее пользователям находить интересные места на карте. Приложение включает в себя функциональность для добавления локаций, загрузки изображений и редактирования описаний с помощью WYSIWYG-редактора. Пользователи могут просматривать информацию о локациях и взаимодействовать с картой.

## 📌 Установка

### 🛠 Предварительные требования

![Версии](https://i.postimg.cc/q7K2DF8t/version2.jpg)

- Python 3.7 или выше
- PostgreSQL (или другая СУБД по вашему выбору)
- Виртуальное окружение (рекомендуется)

### 🔧 Настройка переменных окружения

Для локальной разработки настройка переменных окружения не требуется.
Для разворачивания на production-сервере необходимо создать файл .env корневой директории проекта и добавьте необходимые переменные окружения:

DEBUG=False (В продакшене всегда False)
SECRET_KEY='ваш_секретный_ключ'
DATABASE_URL='sqlite:///db.sqlite3'
ALLOWED_HOSTS='localhost,127.0.0.1,[::1]'
MEDIA_URL='/media/'
MEDIA_ROOT='/path/to/media/'

AWS_STORAGE_BUCKET_NAME='Название S3 Bucket'а'
AWS_S3_CUSTOM_DOMAIN='Название домена AWS CloudFront'
STATIC_URL='/static/'
STATIC_ROOT='/path/to/static/'

**Переменные для https**
Установить в значения:
SECURE_HSTS_SECONDS = <значение в секундах, например 31536000>
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

## 🚀 Запуск

1. 📌 **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/AndreyBychenkow/WhereToGo  
   ```
2. 📌 **Установите зависимости:**

   ```bash
   pip install -r requirements.txt   
   ```
3. 📌 **Примените миграции:**

   ```bash
   python manage.py migrate   
   ```
4. 📌 **Создайте суперпользователя:**

   ```bash
   python manage.py createsuperuser   
   ```
5. 📌 **Запустите сервер:**

   ```bash
   python manage.py runserver   
   ```

Теперь вы можете открыть приложение в браузере по [адресу](http://127.0.0.1:8000/)  и зайти в [админку](http://127.0.0.1:8000/admin/)

Пока на сайте нет локаций. Чтобы поместить новые локации на карту, нужно перейти [сюда](https://github.com/devmanorg/where-to-go-places/tree/master/places), скопировать нужный url и вставить в скрипт.

```bash
   python manage.py load_place <ссылка на распакованные файлы>   
```

В терминале вашей ide отобразится процесс добавления новой локации на карту:

![Успешно](https://github.com/user-attachments/assets/d03a4c4f-026d-4cef-be6e-5ad28903c04c)

После завершения работы скрипта, проверьте результат по [адресу](http://127.0.0.1:8000/) На карте отобразится  новая локация.

![воробьевы карта](https://github.com/user-attachments/assets/0e12dc92-cc1a-4cf5-bfd4-7549be70169c)

При переходе в [адмику](http://127.0.0.1:8000/admin/)   вы так же увидите результат.В списке появится новая локация.

![ВОРОБЬИ АДМИНКА](https://github.com/user-attachments/assets/6c3235c2-78d2-4f95-9db9-6e842760b915)

**Добавляйте новые локации, загружая изображения и редактируя описания с помощью WYSIWYG-редактора.Перетаскивайте изображения, чтобы изменить их порядок**

![Видео-26-01-2025 182748](https://github.com/user-attachments/assets/72ac636c-9f31-4e24-a989-e73ae97336e7)

## ✅ Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org)
