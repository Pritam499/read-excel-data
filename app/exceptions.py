from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

class TableNotFound(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=f"Table '{name}' not found")

class RowNotFound(HTTPException):
    def __init__(self, table: str, row: str):
        super().__init__(status_code=HTTP_404_NOT_FOUND,
                         detail=f"Row '{row}' not found in table '{table}'")

class BadExcel(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=msg)