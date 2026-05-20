SEO Automation System
Automated SEO analytics and weekly reporting for e-commerce.
Status: MVP (Days 1-2 complete) | Python 3.11 | Airflow 2.8 | PostgreSQL 15 | Docker
⚡ Быстрый старт (5 минут)
1. Клонируй репозиторий
bash
Copy
git clone https://github.com/YOUR_USERNAME/seo-automation.git
cd seo-automation
2. Настрой окружение
bash
Copy
# Скопируй шаблон конфигурации
cp .env.example .env

# Отредактируй .env — добавь свои API ключи
nano .env
3. Запусти всё одной командой
bash
Copy
make setup
Это автоматически:
Создаст .env из шаблона
Запустит PostgreSQL, Airflow, Redis
Инициализирует Airflow
Покажет статус всех сервисов
4. Открой Airflow UI
plain
Copy
http://localhost:8080
Логин: airflow / airflow
Найди DAG weekly_seo_report → Toggle ON.
5. Запусти отчёт вручную
bash
Copy
make trigger
Или через Airflow UI: DAG → Trigger DAG.
📋 Требования
Docker 24.0+ и Docker Compose 2.20+
4GB RAM минимум (8GB рекомендуется)
Google Service Account (для GSC, GA4, Sheets)
Yandex OAuth токены
Telegram Bot токен
🛠️ Makefile Команды
Table
Команда	Описание
make setup	Полная настройка (init + up + status)
make init	Инициализация проекта (первый запуск)
make up	Запустить все сервисы
make down	Остановить все сервисы
make restart	Перезапустить
make logs	Смотреть логи всех сервисов
make logs-web	Логи Airflow Webserver
make trigger	Запустить DAG вручную
make status	Статус сервисов и DAGs
make test	Запустить тесты
make shell	Открыть shell в контейнере
make db-shell	PostgreSQL CLI
make backup	Бэкап базы данных
make clean	Удалить ВСЁ (включая данные!)
📁 Структура проекта
plain
Copy
seo-automation/
├── Makefile                          # Все команды проекта
├── docker-compose.yml                # Инфраструктура (Docker)
├── .env.example                      # Шаблон конфигурации
├── pyproject.toml                    # Python metadata
├── requirements.txt                  # Зависимости
│
├── docker/
│   └── Dockerfile                    # Кастомный образ Airflow
│
├── db/
│   └── schema.sql                    # Схема PostgreSQL (12 таблиц)
│
├── airflow/
│   └── dags/
│       └── weekly_seo_report.py    # Основной DAG (воскресенье 8:00)
│
├── src/                              # Исходный код
│   ├── config/
│   │   └── settings.py               # Все настройки из .env
│   ├── extractors/
│   │   ├── gsc_client.py           # Google Search Console API
│   │   ├── ga4_client.py           # Google Analytics 4 API
│   │   ├── yandex_metrika.py       # Яндекс.Метрика API
│   │   ├── yandex_webmaster.py     # Яндекс.Вебмастер API
│   │   └── google_sheets.py        # Google Sheets (кластеры)
│   ├── transformers/
│   │   └── visibility_calculator.py # Псевдо-видимость (веса из .env)
│   ├── loaders/
│   │   └── postgres_loader.py      # PostgreSQL операции
│   ├── analytics/
│   │   └── alerts.py               # Алерт-движок (4 правила)
│   └── reporters/
│       ├── pdf_generator.py        # WeasyPrint + Jinja2 PDF
│       └── telegram_bot.py         # SEO Reports Bot
│
├── templates/
│   └── pdf/
│       └── base.html                 # HTML-шаблон отчёта
│
├── docs/
│   ├── ARCHITECTURE.md             # Архитектура и data flow
│   ├── DEPLOYMENT.md               # Пошаговый деплой
│   └── TROUBLESHOOTING.md          # Решение проблем
│
└── tests/
    └── test_extractors.py          # Unit-тесты
🔧 Конфигурация
Все настройки в .env файле. Ключевые переменные:
Table
Переменная	Описание	Где взять
GOOGLE_SERVICE_ACCOUNT_KEY	Путь к JSON ключу	Google Cloud Console
GSC_SITE_URL	Сайт в GSC	sc-domain:example.com
GA4_PROPERTY_ID	ID свойства GA4	GA4 Admin → Property Settings
YANDEX_METRIKA_TOKEN	OAuth токен	oauth.yandex.ru
TELEGRAM_BOT_TOKEN	Токен бота	@BotFather в Telegram
TELEGRAM_CHAT_ID	ID чата	getUpdates API
SENDGRID_API_KEY	API ключ	sendgrid.com
Настраиваемые веса видимости
В .env можно менять коэффициенты без правки кода:
env
Copy
VISIBILITY_WEIGHT_TOP3=1.0      # Позиции 1-3
VISIBILITY_WEIGHT_TOP10=0.5     # Позиции 4-10
VISIBILITY_WEIGHT_TOP30=0.2     # Позиции 11-30
VISIBILITY_WEIGHT_OTHER=0.0     # Позиции >30
📊 Алерт-правила (настраиваемые)
Table
Правило	Порог	Условие
Падение трафика	−20%	По кластеру/категории за неделю
Падение позиций	−8 пунктов	Ключ с >500 показов/мес
Падение CTR	−30%	За неделю
Crawl errors	Любые	Критические из Я.Вебмастера
Пороги меняются в .env:
env
Copy
ALERT_TRAFFIC_DROP_PCT=20
ALERT_POSITION_DROP_POINTS=8
ALERT_POSITION_MIN_IMPRESSIONS=500
ALERT_CTR_DROP_PCT=30
🚀 Работа с Airflow
Автоматический запуск
DAG weekly_seo_report запускается каждое воскресенье в 8:00.
Ручной запуск
bash
Copy
make trigger
Или через Airflow UI:
Открой http://localhost:8080
Найди weekly_seo_report
Нажми ▶️ Trigger DAG
DAG Structure
plain
Copy
extract_data (TaskGroup)
  ├── extract_gsc        # Google Search Console
  ├── extract_ga4        # Google Analytics 4
  ├── extract_ym         # Яндекс.Метрика
  └── extract_clusters   # Google Sheets
       ↓
transform_data           # Нормализация + агрегация
       ↓
generate_alerts          # Проверка правил
       ↓
generate_report          # PDF отчёт
       ↓
send_notifications       # Telegram + Email
🐛 Troubleshooting
DAG не появляется в UI
bash
Copy
make status              # Проверить статус
make logs-sched          # Логи scheduler
GSC: 403 Forbidden
Добавь service account email в GSC property
Проверь формат GSC_SITE_URL
Yandex: 401 Unauthorized
Токен истёк — пересоздай на oauth.yandex.ru
PDF не генерируется
bash
Copy
make shell
python -c "from weasyprint import HTML; print('OK')"
Полный гайд: docs/TROUBLESHOOTING.md
📈 Roadmap
Table
Этап	Срок	Фичи
MVP	10-12 дней	GSC+GA4+Я.Метрика, кластеры, алерты, PDF, Telegram
2-я ит.	+7-10 дней	Я.Вебмастер, SE Ranking API, z-score, Streamlit
3-я ит.	+5-7 дней	Конкуренты, Looker Studio, ML аномалии
📄 Лицензия
MIT License
