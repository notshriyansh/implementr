from pydantic import BaseModel

class PaperAuthor(BaseModel):
    name: str

class Paper(BaseModel):
    title: str
    summary: str
    pdf_url: str
    published: str
    authors: list[PaperAuthor]

class PaperSearchResponse(BaseModel):
    papers: list[Paper]