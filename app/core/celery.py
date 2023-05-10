from django.conf import settings
import os
from celery import Celery
from celery.schedules import crontab

# from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a CELERY_ prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.timezone = settings.TIME_ZONE
app.conf.task_create_missing_queues = True


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# app.conf.beat_schedule = {
#     "reject-booking-1min": {
#         "task": "reject_booking",
#         "schedule": crontab(minute="*/1"),
#     },
#     "change-status-to-running-1min": {
#         "task": "change_status_to_running",
#         "schedule": crontab(minute="*/1"),
#     },
#     "change-status-to-complete-1min": {
#         "task": "change_status_to_complete",
#         "schedule": crontab(minute="*/1"),
#     },
#     "fetch-all-users-from-hris": {
#         "task": "fetch_all_users_from_hris",
#         "schedule": crontab(hour="9-18", minute="0", day_of_week="1-5"),
#     },
#     "fetch-all-projects-from-hris": {
#         "task": "fetch_all_project_from_smis",
#         "schedule": crontab(hour="9-18", minute="0", day_of_week="1-5"),
#     }
# }
