from pydantic import BaseModel

class DocumentChunk(BaseModel):
    chunk_id: str
    text: str

    page_number: int
    chunk_index: int

    paper_id: str
    user_id: str