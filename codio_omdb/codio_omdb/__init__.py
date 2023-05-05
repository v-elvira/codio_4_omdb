from .celery import app as celery_app

__all__ = ("celery_app",)   # allow Celery to find the app => for @shared_task decorator
