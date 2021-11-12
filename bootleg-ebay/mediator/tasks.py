import socket

from celery import Celery

broker = "amqp://rabbitmq-server"
app = Celery('tasks', broker=broker)

@app.task
def add(x, y):
    return x + y