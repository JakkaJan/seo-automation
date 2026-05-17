# SEO Automation System

Система автоматической еженедельной SEO-аналитики и формирования отчётов.

Автоматически собирает данные из Google Search Console, Google Analytics 4, Яндекс.Метрики и Google Sheets, рассчитывает псевдо-видимость, формирует PDF-отчёт и отправляет его заинтересованным лицам каждое воскресенье в 8:00.

## Возможности

- Сбор и агрегация данных из GSC, GA4 и Яндекс.Метрики
- Маппинг данных по кластерам и категориям из Google Sheets
- Расчёт псевдо-видимости в поисковых системах
- Автоматическое выявление значимых отклонений и алертов
- Генерация профессионального PDF-отчёта с использованием HTML-шаблонов и WeasyPrint
- Рассылка отчётов через Telegram и Email
- Обновление данных в Google Sheets
- Оркестрация процессов через Apache Airflow

## Технологии

- Python 3.11
- Apache Airflow
- PostgreSQL 15
- Docker + docker-compose
- Google APIs (Search Console, Analytics Data, Sheets)
- Яндекс.Метрика API
- WeasyPrint + Jinja2
- Alembic (миграции)

## Структура проекта

```bash
seo-automation/
├── airflow/dags/                    # DAG Airflow
├── src/
│   ├── config/                      # Настройки и credentials
│   ├── extractors/                  # Модули сбора данных
│   ├── transformers/                # Обработка и агрегация
│   ├── loaders/                     # Загрузка в базу данных
│   ├── analytics/                   # Расчёт метрик, алертов и топов
│   ├── reporters/                   # Формирование отчётов и рассылка
│   └── utils/                       # Вспомогательные утилиты
├── templates/pdf/                   # HTML-шаблоны для PDF-отчётов
├── db/migrations/                   # Миграции базы данных (Alembic)
├── docker/                          # Dockerfile и docker-compose.yml
├── docs/                            # Документация
├── tests/                           # Тесты
├── .env.example
├── requirements.txt
├── Makefile
└── pyproject.toml
``