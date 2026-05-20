# =============================================================================
# SEO Automation - Makefile
# =============================================================================

.PHONY: help up down logs init test clean restart trigger status shell

# Default target
help:
	@echo "SEO Automation - Available commands:"
	@echo ""
	@echo "  make init       - Initialize project (first run)"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs from all services"
	@echo "  make logs-web   - View Airflow webserver logs"
	@echo "  make logs-sched - View Airflow scheduler logs"
	@echo "  make test       - Run tests"
	@echo "  make trigger    - Manually trigger weekly report DAG"
	@echo "  make status     - Check service status"
	@echo "  make shell      - Open shell in airflow container"
	@echo "  make clean      - Remove all containers and volumes (DANGER)"
	@echo "  make setup      - Full setup: init + up + status"
	@echo ""

# Environment setup
init:
	@echo "Initializing SEO Automation..."
	cp -n .env.example .env || true
	@echo "Created .env from template. Please edit it with your credentials."
	export AIRFLOW_UID=$$(id -u) && docker-compose up -d airflow-init
	@echo "Airflow initialized. Waiting for services..."
	@sleep 10

# Start services
up:
	export AIRFLOW_UID=$$(id -u) && docker-compose up -d
	@echo "Services starting..."
	@sleep 5
	@echo "Airflow UI: http://localhost:8080 (login: airflow / airflow)"

# Stop services
down:
	docker-compose down

# Restart services
restart: down up

# View logs
logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f airflow-webserver

logs-sched:
	docker-compose logs -f airflow-scheduler

# Run tests
test:
	docker-compose exec airflow-worker pytest tests/ -v

# Manual DAG trigger
trigger:
	@echo "Triggering weekly_seo_report DAG..."
	docker-compose exec airflow-scheduler airflow dags trigger weekly_seo_report
	@echo "DAG triggered. Check Airflow UI for status."

# Check status
status:
	@echo "=== Docker Containers ==="
	@docker-compose ps
	@echo ""
	@echo "=== Airflow DAGs ==="
	@docker-compose exec airflow-scheduler airflow dags list 2>/dev/null || echo "Airflow not ready yet, wait 30 seconds..."

# Open shell
shell:
	docker-compose exec airflow-worker bash

# Database shell
db-shell:
	docker-compose exec postgres psql -U airflow -d airflow

# Clean everything (DANGER - removes data!)
clean:
	@echo "WARNING: This will remove all containers and volumes!"
	@echo "Press Ctrl+C to cancel, or wait 5 seconds..."
	@sleep 5
	docker-compose down -v
	docker system prune -f
	@echo "Cleaned. Run 'make init' to start fresh."

# Full setup
setup: init up status
	@echo ""
	@echo "Setup complete! Next steps:"
	@echo "1. Edit .env with your credentials"
	@echo "2. Place Google service account JSON in secrets/"
	@echo "3. Visit http://localhost:8080 and enable weekly_seo_report DAG"
	@echo "4. Run 'make trigger' to test manually"

# Backup database
backup:
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U airflow airflow > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backups/"

# Development helpers
format:
	docker-compose exec airflow-worker black src/ tests/

lint:
	docker-compose exec airflow-worker flake8 src/ tests/
