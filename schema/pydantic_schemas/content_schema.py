from pydantic import BaseModel

class ContentSchema(BaseModel):
    content: str | None = None