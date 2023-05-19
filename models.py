from pydantic import BaseModel


class PendingClassification(BaseModel):
    task_id: str
    status: str


class ClassificationResult(BaseModel):
    task_id: str
    status: str
    predicted_class: int