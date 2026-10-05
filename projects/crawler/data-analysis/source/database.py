from dataclasses import dataclass
from pathlib import Path
import pandas as pd

from .base import DataSource



@dataclass(slots=True)
class DuckDBQuery(DataSource):
    database: Path
    query: str

    def read(self) -> pd.DataFrame:
        import duckdb

        return duckdb.sql(
            self.query,
        ).df()