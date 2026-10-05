from dataclasses import dataclass
from pathlib import Path
import pandas as pd

from .base import DataSource


@dataclass(slots=True)
class CSVFile(DataSource):
    path: Path

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

@dataclass(slots=True)
class JSONFile(DataSource):
    path: Path

    def read(self) -> pd.DataFrame:
        return pd.read_json(self.path)

@dataclass(slots=True)
class ExcelFile(DataSource):
    path: Path
    sheet_name: str | int = 0

    def read(self) -> pd.DataFrame:
        return pd.read_excel(
            self.path,
            sheet_name=self.sheet_name,
        )