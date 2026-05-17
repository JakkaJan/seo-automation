# Deployment Guide

## Server Requirements

- Ubuntu 24.04 (tested)
- 4 vCPU, 8GB RAM, 100GB SSD (minimum)
- Docker 24.0+ and Docker Compose 2.20+

## Step-by-Step Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt install docker-compose-plugin
```

### 2. Clone Repository

```bash
git clone <repo-url> /opt/seo-automation
cd /opt/seo-automation
```

### 3. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit all values
```

### 4. Upload Credentials

```bash
mkdir -p secrets
# Upload Google service account JSON
# Upload any other credential files
chmod 600 secrets/*
```

### 5. Start Services

```bash
export AIRFLOW_UID=$(id -u)
docker-compose up -d airflow-init
# Wait 30 seconds
docker-compose up -d
```

### 6. Verify

```bash
docker-compose ps
docker-compose logs -f airflow-webserver
```

### 7. Configure Airflow

```bash
# Access UI at http://your-server:8080
# Login: airflow / airflow (change in production!)

# Add PostgreSQL connection
docker exec -it airflow-webserver airflow connections add 'postgres_default' \
    --conn-type 'postgres' \
    --conn-host 'postgres' \
    --conn-port '5432' \
    --conn-login 'airflow' \
    --conn-password 'airflow'
```

### 8. Enable DAG

In Airflow UI:
1. Go to DAGs
2. Find `weekly_seo_report`
3. Toggle ON
4. Verify schedule shows "0 8 * * 0"

## Production Hardening

- Change default Airflow credentials
- Enable HTTPS (nginx reverse proxy + Let's Encrypt)
- Set up log rotation
- Configure backup for PostgreSQL volume
- Use secrets manager for sensitive data

## Backup

```bash
# Backup database
docker exec -it seo-automation-postgres-1 pg_dump -U airflow airflow > backup_$(date +%Y%m%d).sql

# Backup reports
tar -czf reports_backup_$(date +%Y%m%d).tar.gz reports/
```
