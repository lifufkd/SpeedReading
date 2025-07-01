from datetime import datetime
from pydantic import BaseModel


class TimestampedSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
