import uuid
from django.db import models
from datetime import datetime
class UUIDTimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())

    class Meta:
        abstract = True