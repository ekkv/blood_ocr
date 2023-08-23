# celery -A tasks worker -l Info -P eventlet --concurrency=4

import logging
from celery import Celery, Task

from redis import Redis
from d_ocr import donation_ocr


redis_conn = 'redis://redis:6379'

worker = Celery('work',
                broker=redis_conn,
                backend=redis_conn
                )


class PredictTask(Task):
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            logging.info('Loading Model...')
            self.model = donation_ocr()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask)
def process_image(self, img_id):
    result = self.model.predict(img_id)
    return result
