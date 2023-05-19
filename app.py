from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from celery.result import AsyncResult

from celery_task_app.tasks import predict_data
from models import ClassificationResult, PendingClassification

app = FastAPI()


@app.post('/predict', response_model=PendingClassification, status_code=202)
async def model(file: UploadFile):
    temp_file = f"media/{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())
    task_id = predict_data.delay(temp_file)
    return {'task_id': str(task_id), 'status': f'Processing'}


@app.get('/result/{task_id}', response_model=ClassificationResult, status_code=200,
         responses={202: {'model': PendingClassification, 'description': 'Accepted: Not Ready'}})
async def model_result(task_id):
    task = AsyncResult(task_id)
    if not task.ready():
        print(app.url_path_for('model'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': 'Success', 'predicted_class': str(result)}

