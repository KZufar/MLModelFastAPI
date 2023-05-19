import importlib
import logging

import numpy as np
from PIL import Image
from celery import Task

from .worker import app


class PredictTask(Task):
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            logging.info('Loading Model...')
            module_import = importlib.import_module(self.path[0])
            model_obj = getattr(module_import, self.path[1])
            self.model = model_obj()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@app.task(ignore_result=False,
          bind=True,
          base=PredictTask,
          path=('celery_task_app.ml.model', 'MNISTModel'),
          name='{}.{}'.format(__name__, 'Model'))
def predict_data(self, img_file):
    logging.info('Predict...')
    img = Image.open(img_file)
    image_data = np.array(img)
    pred_array = self.model.predict(image_data)
    return pred_array
