# link-shortener-FastAPI
Сервис сокращения ссылок на FastAPI с PostgreSQL, JWT авторизацией и Docker.

## Запуск

### Локально
1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите: `uvicorn src.main:app --reload`

### С Docker
1. `docker-compose up --build`

## API

### Авторизация
- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Логин, возвращает JWT токен

### Ссылки
- `POST /shorten` - Создать короткую ссылку (требует авторизации)
- `GET /go/{short_code}` - Переход по короткой ссылке
- `GET /link/{short_code}/info` - Информация о ссылке
- `DELETE /link/{short_code}` - Удалить ссылку
- `GET /links` - Все ссылки

Используйте токен в заголовке: `Authorization: Bearer <token>`

## Документация API
Доступна по `/docs` после запуска.

## Надо сделать

* Исправить ошибки
* PostgresQL ☑
* Docker ☑
* JWT ☑
* Документация ☑
* Мониторинг (Grafana + Prometheus)
