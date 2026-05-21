from datetime import datetime

from pydantic import BaseModel


class ReportResponse(BaseModel):
    format: str = "markdown"
    generated_at: datetime
    markdown: str
