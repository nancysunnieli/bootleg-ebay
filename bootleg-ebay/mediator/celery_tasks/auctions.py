import celery

@celery.shared_task(name='celery_tasks.add_together')
# @celery.shared_task
def add_together(x, y):
    return x + y