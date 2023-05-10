from .base import *
import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "debug.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "propagate": True,
            "level": "INFO",
        },
        "MYAPP": {
            "handlers": ["file"],
            "level": "INFO",
        },
    },
}

sentry_sdk.init(
    dsn=config("DSN_KEY"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
