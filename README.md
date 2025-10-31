# link-shortener-FastAPI
Сервис сокращения ссылок на FastAPI с PostgreSQL, JWT авторизацией, Docker и мониторингом через Grafana + Prometheus.

## Запуск

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
- `DELETE /link/{short_code}` - Удалить ссылку (требует авторизации)
- `GET /links` - Все ссылки

Используйте токен в заголовке: `Authorization: Bearer <token>`

## Документация API
Доступна по `/docs` после запуска.

## Мониторинг

Проект включает настройку мониторинга с использованием Prometheus и Grafana.

### Prometheus
- Собирает метрики с приложения по эндпоинту `/metrics`
- Метрики включают: количество HTTP запросов, время ответа, статус коды
- Доступен по адресу: `http://localhost:9090`

### Grafana
- Визуализирует метрики из Prometheus
- Доступен по адресу: `http://localhost:3000`
- Логин: `admin`, Пароль: `admin`
- Дашборды можно создавать для отслеживания производительности API