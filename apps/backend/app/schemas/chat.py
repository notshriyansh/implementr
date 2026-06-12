from pydantic import BaseModel

class Citation(BaseModel):
    paper_id: str
    page_number: int
    chunk_index: int

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]