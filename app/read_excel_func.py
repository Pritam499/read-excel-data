import pandas as pd
from pandas import ExcelFile
from typing import List, Optional

class ExcelProcessingError(Exception):
    pass

class ExcelReader:
    def __init__(self, path: str):
        try:
            self._xls = ExcelFile(path)
        except Exception as e:
            raise ExcelProcessingError(f"Failed to open Excel file: {e}")

    def list_tables(self) -> List[str]:
        """Return sheet names."""
        return self._xls.sheet_names

    def get_dataframe(self, table_name: str) -> pd.DataFrame:
        if table_name not in self._xls.sheet_names:
            raise ExcelProcessingError(f"Table '{table_name}' not found")
        return self._xls.parse(table_name)

    def get_row_names(self, table_name: str) -> List[str]:
        df = self.get_dataframe(table_name)
        if df.shape[1] < 1:
            raise ExcelProcessingError(f"Table '{table_name}' has no columns")
        # First column all values (as strings)
        return df.iloc[:, 0].astype(str).tolist()

    def sum_row(self, table_name: str, row_name: str) -> float:
        df = self.get_dataframe(table_name)
        # Find matching row(s) in the first column
        mask = df.iloc[:, 0].astype(str) == row_name
        if not mask.any():
            raise ExcelProcessingError(f"Row '{row_name}' not found in table '{table_name}'")
        row = df.loc[mask, df.columns[1:]]  # drop first column
        # Coerce to numeric; ignore non-numeric
        nums = pd.to_numeric(row.values.flatten(), errors="coerce")
        return float(nums[~pd.isna(nums)].sum())
