from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from app.read_excel_func import ExcelReader, ExcelProcessingError
from app.schemas import TablesList, TableDetails, RowSum, ErrorResponse
from app.exceptions import TableNotFound, RowNotFound, BadExcel

import os

app = FastAPI(title="Read Excel Data API")

# Load workbook on startup
@app.on_event("startup")
def load_workbook():
    path = os.getenv("EXCEL_PATH", "data/capbudg.xls")
    try:
        app.state.reader = ExcelReader(path)
    except ExcelProcessingError as e:
        # If the file is missing or unreadable, we fail fast
        raise BadExcel(str(e))

def get_reader() -> ExcelReader:
    return app.state.reader

@app.get("/list_tables", response_model=TablesList, responses={400: {"model": ErrorResponse}})
def list_tables(reader: ExcelReader = Depends(get_reader)):
    try:
        tables = reader.list_tables()
        return {"tables": tables}
    except ExcelProcessingError as e:
        raise BadExcel(str(e))

@app.get("/get_table_details", response_model=TableDetails,
         responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}})
def get_table_details(
    table_name: str = Query(..., description="Name of the sheet/table"),
    reader: ExcelReader = Depends(get_reader),
):
    try:
        rows = reader.get_row_names(table_name)
    except ExcelProcessingError as e:
        msg = str(e)
        if "not found" in msg:
            raise TableNotFound(table_name)
        else:
            raise BadExcel(msg)
    return {"table_name": table_name, "row_names": rows}

@app.get("/get_row_sum", response_model=RowSum,
         responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}})
def get_row_sum(
    table_name: str = Query(...),
    row_name: str = Query(...),
    reader: ExcelReader = Depends(get_reader),
):
    try:
        total = reader.sum_row(table_name, row_name)
    except ExcelProcessingError as e:
        msg = str(e)
        if "Table" in msg and "not found" in msg:
            raise TableNotFound(table_name)
        if "Row" in msg and "not found" in msg:
            raise RowNotFound(table_name, row_name)
        else:
            raise BadExcel(msg)
    return {"table_name": table_name, "row_name": row_name, "sum": total}
