from decouple import config

if config('ENVIRONMENT') == 'development':
    from .development import *
else:
    from .production import *
