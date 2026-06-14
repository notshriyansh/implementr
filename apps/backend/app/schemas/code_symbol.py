from pydantic import BaseModel


class CodeSymbol(BaseModel):
    symbol_id: str
    file_path: str
    symbol_name: str
    symbol_type: str
    code: str
    start_line: int
    end_line: int