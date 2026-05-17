# Troubleshooting Guide

## Common Issues

### DAG Not Appearing in Airflow UI

**Symptom**: `weekly_seo_report` not visible

**Solution**:
```bash
# Check DAG parsing
docker exec -it airflow-scheduler airflow dags list

# Check for syntax errors
docker exec -it airflow-scheduler python -m py_compile dags/weekly_seo_report.py

# Restart scheduler
docker-compose restart airflow-scheduler
```

### GSC API Errors

**Error**: `403 Forbidden` or `site not found`

**Solution**:
1. Verify service account email added to GSC property
2. Check `GSC_SITE_URL` format:
   - Domain property: `sc-domain:example.com`
   - URL prefix: `https://example.com/`
3. Ensure property has data for requested date range

### Yandex Metrika Token Expired

**Error**: `401 Unauthorized`

**Solution**:
1. Go to https://oauth.yandex.ru
2. Generate new token with `metrika:read` scope
3. Update `YANDEX_METRIKA_TOKEN` in `.env`
4. Restart: `docker-compose restart`

### PDF Generation Fails

**Error**: `OSError: cannot load library`

**Solution**:
```bash
# Rebuild with all dependencies
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Issues

**Error**: `connection refused` or `database does not exist`

**Solution**:
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Reinitialize
docker-compose down -v
docker-compose up -d airflow-init
docker-compose up -d
```

### Telegram Bot Not Sending Messages

**Error**: No messages received

**Solution**:
1. Verify bot token with: `curl https://api.telegram.org/bot<TOKEN>/getMe`
2. Start chat with bot first
3. Get chat ID: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Update `TELEGRAM_CHAT_ID`

## Debug Mode

Enable verbose logging:

```python
# In .env
LOG_LEVEL=DEBUG
```

Check logs:
```bash
docker-compose logs -f airflow-worker
docker-compose logs -f airflow-scheduler
```

## Getting Help

1. Check Airflow task logs in UI (Admin → Logs)
2. Check application logs: `logs/seo_automation.log`
3. Verify all `.env` values are set correctly
4. Test individual components:
   ```bash
   docker exec -it airflow-worker python -c "from src.extractors import GSCClient; print('OK')"
   ```
