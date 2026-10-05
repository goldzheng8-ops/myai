from abc import ABC, abstractmethod

import pandas as pd


class DataSource(ABC):

    @abstractmethod
    def read(self) -> pd.DataFrame:
        ...