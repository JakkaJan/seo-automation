# SEO Automation System

```bash Цена заказа 2400$ + 180$ на поддержание каждый месяц ```


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
├── airflow/
│   └── dags/
│       └── weekly_seo_report_dag.py
├── src/
│   ├── config/
│   │   ├── settings.py
│   │   └── credentials.py
│   ├── extractors/
│   │   ├── gsc_client.py
│   │   ├── ga4_client.py
│   │   ├── yandex_metrika.py
│   │   ├── yandex_webmaster.py
│   │   └── google_sheets.py
│   ├── transformers/
│   │   ├── normalizer.py
│   │   ├── aggregator.py
│   │   └── visibility_calculator.py
│   ├── loaders/
│   │   └── postgres_loader.py
│   ├── analytics/
│   │   ├── metrics.py
│   │   ├── alerts.py
│   │   └── tops.py
│   ├── reporters/
│   │   ├── pdf_generator.py
│   │   ├── sheets_reporter.py
│   │   └── telegram_bot.py
│   └── utils/
│       ├── logger.py
│       └── date_helpers.py
├── db/
│   ├── migrations/
│   └── schema.sql
├── templates/
│   └── pdf/
│       ├── base.html
│       ├── cover.html
│       ├── dashboard.html
│       ├── clusters.html
│       ├── tops.html
│       └── alerts.html
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── TROUBLESHOOTING.md
├── .env.example
├── requirements.txt
├── pyproject.toml
└── Makefile
