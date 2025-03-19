# FlaskAuth-API

## Описание проекта

FlaskAuth-API — это REST API для аутентификации и управления контентом, реализованное на Flask с использованием PostgreSQL и Redis. Проект поддерживает ролевую модель пользователей (user, admin).

---

## 1. Установка и запуск проекта

### **Установка зависимостей**

Клонируем репозиторий:

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd FlaskAuth-API
```

Создаём виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### **Конфигурация окружения**

Создаём `.env` файл и добавляем параметры:

```bash
touch .env
nano .env
```

Пример `.env`:

```ini
DB_NAME=flask_auth_db
DB_USER=flask_user
DB_PASSWORD=123456
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

JWT_SECRET_KEY=supersecretkey
JWT_ACCESS_TOKEN_EXPIRES=3600

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

---

## 2. Запуск проекта в Docker

Запускаем контейнеры с базой данных, сервером и Redis:

```bash
sudo docker-compose up --build -d
```

Проверяем запущенные контейнеры:

```bash
docker ps
```

---

## Создание администратора

При первом запуске **автоматически создаётся** администратор с логином `admin` и паролем `adminpassword`.
Файл _init_admin.py_ отвечает за инициализацию администратора при первом запуске. При необходимости измените настройки вручную тут:
```bash
nano app/init_admin.py
```
Если нужно создать нового админа вручную:

---

## 3. Тестирование API

### **Авторизация (JWT)**

**Регистрация пользователя:**

```bash
curl -X POST "http://localhost:5000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "testpass"}'
```

**Логин:**

```bash
curl -X POST "http://localhost:5000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "testpass"}'
```

В ответе будет `access_token`, который нужно использовать для авторизации.

### **Доступ к защищённым ресурсам**

**Получение контента (требуется токен):**

```bash
curl -X GET "http://localhost:5000/api/content" \
     -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 4. Структура проекта

```bash
.
├── app                 # Основная логика API
│   ├── api             # Эндпоинты
│   ├── models          # Модели данных (SQLAlchemy)
│   ├── services        # Бизнес-логика
│   ├── repositories    # Работа с БД
│   ├── utils           # Вспомогательные утилиты
│   ├── database.py     # Подключение к БД
│   ├── config.py       # Конфигурация
│   ├── main.py         # Точка входа в приложение
│   └── init_admin.py   # Создание администратора
├── migrations          # Миграции Alembic
├── Dockerfile          # Docker-сборка
├── docker-compose.yml  # Запуск в контейнерах
├── requirements.txt    # Зависимости
├── README.md           # Документация
└── .gitignore          # Исключения Git
```

---

## 5. Полезные команды

### **Перезапуск приложения**

```bash
sudo docker-compose down -v && sudo docker-compose up --build -d
```

### **Просмотр логов**

```bash
docker logs -f flask_auth_api
```

### **Очистка контейнеров и данных**

```bash
sudo docker-compose down -v
```

---
