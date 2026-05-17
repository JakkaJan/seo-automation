# SEO Automation System

``` Цена заказа 2400$ + 180$ на поддержание каждый месяц согласно согласованной документации```


Система автоматической еженедельной SEO-аналитики и формирования отчётов для интернет-магазина.

Автоматически собирает данные из Google Search Console, Google Analytics 4, Яндекс.Метрики, Google Sheets и формирует красивый PDF-отчёт каждое воскресенье в 8:00.

## Основные возможности

- Еженедельный сбор данных из GSC, GA4 и Яндекс.Метрики
- Агрегация трафика и позиций по кластерам и категориям
- Расчёт псевдо-видимости в поисковых системах
- Автоматические алерты при значимых падениях
- Генерация красивого PDF-отчёта (WeasyPrint + HTML/CSS)
- Отправка отчёта в Telegram и Email
- Обновление Google Sheets
- Полностью контейнеризировано (Docker + Airflow)

## Технологии

- **Python 3.11**
- **Airflow** — оркестрация
- **PostgreSQL 15** — хранение данных
- **Docker + docker-compose**
- **Google APIs** (Search Console, Analytics Data, Sheets)
- **Яндекс.Метрика API**
- **WeasyPrint + Jinja2** — генерация PDF
- **python-telegram-bot**, SendGrid

## Структура проекта

```bash
seo-automation/
├── airflow/dags/              # DAG-файлы
├── src/
│   ├── config/
│   ├── extractors/            # GSC, GA4, Я.Метрика и т.д.
│   ├── transformers/
│   ├── loaders/
│   ├── analytics/
│   ├── reporters/             # PDF, Telegram, Email
│   └── utils/
├── templates/pdf/             # HTML-шаблоны отчётов
├── db/migrations/             # Alembic
├── docker/                    # Dockerfile, docker-compose.yml
├── docs/                      # Документация
├── tests/
├── .env.example
├── requirements.txt
├── Makefile
└── pyproject.toml