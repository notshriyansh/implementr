from pydantic import BaseModel

class DocumentPage(BaseModel):
    page_number: int
    text: str

class ParsedDocument(BaseModel):
    pages: list[DocumentPage]
    total_pages: int