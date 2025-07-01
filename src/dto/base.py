from datetime import datetime
from pydantic import BaseModel


class TimestampedDTO(BaseModel):
    created_at: datetime
    updated_at: datetime
