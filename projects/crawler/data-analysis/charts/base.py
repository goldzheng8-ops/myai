from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure


class Chart(ABC):
    """
    Base interface for all charts.
    """

    @abstractmethod
    def render(self, data: pd.DataFrame) -> Figure:
        """
        Render the chart from tabular data.
        """
        ...

    def save(
        self,
        data: pd.DataFrame,
        path: str | Path,
        *,
        dpi: int = 150,
        **kwargs, # type: ignore
    ) -> None:
        """
        Render and save the chart.
        """
        figure = self.render(data)
        figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs) # type: ignore