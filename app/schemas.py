from pydantic import BaseModel
from typing import List

class TablesList(BaseModel):
    tables: List[str]

class TableDetails(BaseModel):
    table_name: str
    row_names: List[str]

class RowSum(BaseModel):
    table_name: str
    row_name: str
    sum: float

class ErrorResponse(BaseModel):
    detail: str
