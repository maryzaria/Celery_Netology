import os

from celery import Celery

BACKEND = os.getenv("BACKEND")
BROKER = os.getenv("BROKER")

celery_app = Celery(broker=BROKER, backend=BACKEND)
