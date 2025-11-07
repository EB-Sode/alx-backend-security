from celery import Celery
from celery.schedules import crontab

app = Celery('your_project_name')

app.conf.beat_schedule = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': crontab(minute=0, hour='*'),  # every hour
    },
}
