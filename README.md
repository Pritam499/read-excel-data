# read-excel-data
Read Data from given excel file using GET Request.

OVERVIEW
This service exposes three HTTP GET endpoints to read data from an Excel file (“capbudg.xls”), list available sheets (“tables”), list the row headers in a sheet, and compute the numeric sum of a particular row. It is built with FastAPI and Pandas.

PREREQUISITES
• Python 3.8 or later installed on your machine
• Git client (for cloning the repository)
• Internet connection (to install dependencies)
• A copy of your Excel file named capbudg.xls

REPOSITORY STRUCTURE
(read-excel-data/)
├ app/
│ ├ main.py ← FastAPI application and route definitions
│ ├ read_excel_utils.py ← ExcelReader class (loads workbook, lists sheets, reads rows, sums values)
│ ├ schemas.py ← Pydantic models for request/response payloads
│ └ exceptions.py ← Custom HTTPException subclasses for 404/400 errors
├ data/
│ └ capbudg.xls ← Place your production Excel workbook here

STEP-BY-STEP SETUP

A. Clone the repo
git clone https://github.com/Pritam499/read-excel-data.git
cd read-excel-data

B. Create a virtual environment
On Windows (cmd.exe):
python -m venv .venv


C. Activate the virtual environment
Windows cmd.exe:
.venv\Scripts\activate

D. Install dependencies
pip install fastapi uvicorn pandas openpyxl xlrd

E. Place your Excel file
Copy capbudg.xls file into the data/ folder so the path is data/capbudg.xls


CODE WALKTHROUGH

A. read_excel_utils.py
• ExcelReader class
– init(path)
• Tries to open the workbook via pandas.ExcelFile(path).
• Raises ExcelProcessingError on failure (missing file, bad format).
– list_tables() → List[str]
• Returns sheet_names from the workbook.
– get_dataframe(table_name) → DataFrame
• Validates sheet exists; parses it to a DataFrame.
– get_row_names(table_name) → List[str]
• Loads the sheet, then returns all values in the first column as strings.
– sum_row(table_name, row_name) → float
• Selects rows whose first‐column value equals row_name.
• Converts cells in all subsequent columns to numeric (coerce errors→NaN).
• Sums the non-NaN values and returns the total.

B. exceptions.py
• TableNotFound(name) → HTTPException 404 with message “Table ‘name’ not found”
• RowNotFound(table, row) → HTTPException 404 with message “Row ‘row’ not found in table ‘table’”
• BadExcel(msg) → HTTPException 400 for any other Excel-related errors

C. schemas.py
• TablesList: { tables: List[str] }
• TableDetails: { table_name: str; row_names: List[str] }
• RowSum: { table_name: str; row_name: str; sum: float }
• ErrorResponse: { detail: str }

D. main.py
• FastAPI() instance created with title “Read Excel Data API”
• @app.on_event("startup") load_workbook()
– Reads EXCEL_PATH or defaults to data/capbudg.xls
– Instantiates ExcelReader and attaches it to app.state.reader
– On failure, raises BadExcel so the server won’t start
• Dependency get_reader() returns the shared ExcelReader
• Route /list_tables
– Uses reader.list_tables()
– Returns TablesList model or 400 on error
• Route /get_table_details
– Query param: table_name
– Uses reader.get_row_names(table_name)
– Returns TableDetails or 404 if table missing
• Route /get_row_sum
– Query params: table_name, row_name
– Uses reader.sum_row()
– Returns RowSum or 404 if table/row missing

RUNNING THE SERVICE

With your .venv activated and Excel file in place:

uvicorn app.main:app --reload --host 0.0.0.0 --port 9090

Watch for logs:

– “Waiting for application startup.”
– “Uvicorn running on http://0.0.0.0:9090”

Test Using POSTMAN 

• {{base_url}} = http://localhost:9090
• {{table}} = (name of a sheet from /list_tables)
• {{row}} = (one of the row_names from /get_table_details)

ROUTES SUMMARY

LIST TABLES
URL
GET http://localhost:9090/list_tables
Query parameters
none
Response 200
{
    "tables": [
        "CapBudgWS"
    ]
}

GET TABLE DETAILS
URL
GET http://localhost:9090/get_table_details?table_name=CapBudgWS
Query parameters
table_name=CapBudgWS
Response 200
{
    "table_name": "CapBudgWS",
    "row_names": [
        "nan",
        "INITIAL INVESTMENT",
        "Initial Investment=",
        "Opportunity cost (if any)=",
        "Lifetime of the investment",
        "Salvage Value at end of project=",
        "Deprec. method(1:St.line;2:DDB)=",
        "Tax Credit (if any )=",
        "Other invest.(non-depreciable)=",
        "nan",
        "WORKING CAPITAL",
        "Initial Investment in Work. Cap=",
        "Working Capital as % of Rev=",
        "Salvageable fraction at end=",
        "nan",
        "GROWTH RATES",
        "nan",
        "Revenues",
        "Fixed Expenses",
        "Default: The fixed expense growth rate is set equal to the growth rate in revenues by default.",
        "nan",
        "nan",
        "INITIAL INVESTMENT",
        "Investment",
        " - Tax Credit",
        "Net Investment",
        " + Working Cap",
        " + Opp. Cost",
        " + Other invest.",
        "Initial Investment",
        "nan",
        "SALVAGE VALUE",
        "Equipment",
        "Working Capital",
        "nan",
        "OPERATING CASHFLOWS",
        "Lifetime Index",
        "Revenues",
        " -Var. Expenses",
        " - Fixed Expenses",
        "EBITDA",
        " - Depreciation",
        "EBIT",
        " -Tax",
        "EBIT(1-t)",
        " + Depreciation",
        " - ∂ Work. Cap",
        "NATCF",
        "Discount Factor",
        "Discounted CF",
        "nan",
        "nan",
        "nan",
        "nan",
        "nan",
        "nan",
        "nan",
        "nan",
        "Book Value (beginning)",
        "Depreciation",
        "BV(ending)"
    ]
}

GET ROW SUM
URL
GET http://localhost:9090/get_row_sum?table_name=CapBudgWS&row_name=NATCF
Query parameters
table_name=CapBudgWS
row_name=NATCF
Response 200
{
    "table_name": "CapBudgWS",
    "row_name": "NATCF",
    "sum": 109982.20000000007
}