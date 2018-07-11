from celery import Celery

app = Celery('tasks',
             broker='redis://10.71.2.138',
             backend='redis://10.71.2.138')

@app.task
def add(x, y):
    print("running...", x, y)
    return x + y