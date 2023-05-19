# ServingMLFastCelery
Working example for serving a ML model using FastAPI and Celery.

## Usage

**Install requirements:**
```bash
pip install -r requirements.txt
```

**Start API:**
```bash
uvicorn app:app
```

**Start worker node:**
```bash
celery -A celery_task_app.worker worker -l info
```

**API methods**
```bash
curl -X POST 'http://localhost:8000/predict' --form 'file=@"{your_image_path}"'
```

```bash
curl -X GET 'http://localhost:8000/result/{your_task_id}'
```

**Run Test**
```bash
python test.py
```

