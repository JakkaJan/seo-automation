&lt;div align="center"&gt;

# 📊 SEO Automation System

### Автоматизированная SEO-аналитика и еженедельная отчётность

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://python.org)
[![Airflow](https://img.shields.io/badge/Airflow-2.8-green?logo=apacheairflow)](https://airflow.apache.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Статус:** MVP (Дни 1-2 ✅) | **Стек:** Python 3.11 · Airflow 2.8 · PostgreSQL 15 · Docker

&lt;/div&gt;

---

## ✨ Возможности

| 🚀 Автоматизация | 📈 Аналитика | 🚨 Мониторинг | 📄 Отчётность |
|:---|:---|:---|:---|
| Сбор данных каждое воскресенье в 8:00 | Органический трафик, позиции, CTR | Алерты на критические отклонения | Красивый PDF + Telegram + Email |
| GSC · GA4 · Я.Метрика · Я.Вебмастер | Группировка по кластерам | Падение трафика &gt;20% | Google Sheets обновление |
| Ручной запуск одной командой | Псевдо-видимость с настраиваемыми весами | Падение позиций &gt;8 пунктов | Современный дизайн WeasyPrint |

---

## ⚡ Быстрый старт (5 минут)

### 1️⃣ Клонируй репозиторий

```bash
git clone https://github.com/YOUR_USERNAME/seo-automation.git
cd seo-automation
```
2️⃣ Настрой окружение
```bash
cp .env.example .env
nano .env
```
3️⃣ Запусти всё одной командой
```bash
make setup
```
4️⃣ Открой Airflow UI
```bash
🌐 http://localhost:8080
👤 Логин: airflow / airflow
```
5️⃣ Запусти отчёт вручную
```bash
make trigger
```
| Команда | Описание |
|:---|:---|
|make setup|🚀 Полная настройка (init + up + status)|
|make init|🏗️ Инициализация проекта (первый запуск)|
|make up|▶️ Запустить все сервисы|
|make down|⏹️ Остановить все сервисы|
|make restart|🔄 Перезапустить|
|make logs|📋 Смотреть логи всех сервисов|
|make logs-web|🌐 Логи Airflow Webserver|
|make trigger|⚡ Запустить DAG вручную|
|make status|📊 Статус сервисов и DAGs|
|make test|🧪 Запустить тесты|
|make shell|🐚 Открыть shell в контейнере|
|make db-shell|🐘 PostgreSQL CLI|
|make backup|💾 Бэкап базы данных|
|make clean|🧹 Удалить ВСЁ (включая данные!)|
```bash
seo-automation/
├── 📄 Makefile                          # Все команды проекта
├── 🐳 docker-compose.yml                # Инфраструктура
├── ⚙️ .env.example                      # Шаблон конфигурации
├── 📦 pyproject.toml                    # Python metadata
│
├── 🐳 docker/
│   └── Dockerfile                       # Кастомный образ Airflow
│
├── 🐘 db/
│   └── schema.sql                       # Схема PostgreSQL (12 таблиц)
│
├── 🌪️ airflow/
│   └── dags/
│       └── weekly_seo_report.py         # Основной DAG
│
├── 💻 src/                              # Исходный код
│   ├── ⚙️ config/
│   │   └── settings.py                  # Настройки из .env
│   ├── 🔌 extractors/
│   │   ├── gsc_client.py                # Google Search Console
│   │   ├── ga4_client.py                # Google Analytics 4
│   │   ├── yandex_metrika.py            # Яндекс.Метрика
│   │   ├── yandex_webmaster.py          # Яндекс.Вебмастер
│   │   └── google_sheets.py             # Google Sheets (кластеры)
│   ├── 🔄 transformers/
│   │   └── visibility_calculator.py     # Псевдо-видимость
│   ├── 💾 loaders/
│   │   └── postgres_loader.py           # PostgreSQL операции
│   ├── 📊 analytics/
│   │   └── alerts.py                    # Алерт-движок
│   └── 📄 reporters/
│       ├── pdf_generator.py             # WeasyPrint PDF
│       └── telegram_bot.py              # SEO Reports Bot
│
├── 🎨 templates/
│   └── pdf/
│       └── base.html                    # HTML-шаблон отчёта
│
├── 📚 docs/
│   ├── ARCHITECTURE.md                  # Архитектура
│   ├── DEPLOYMENT.md                    # Деплой
│   └── TROUBLESHOOTING.md               # Решение проблем
│
└── 🧪 tests/
    └── test_extractors.py               # Unit-тесты

```
