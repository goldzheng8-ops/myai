from dataclasses import dataclass

import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .base import Chart

@dataclass(slots=True)
class LineChart(Chart):
    x: str
    y: str
    title: str | None = None
    xlabel: str | None = None
    ylabel: str | None = None

    def render(self, data: pd.DataFrame) -> Figure:
        figure, axis = plt.subplots()

        axis.plot(
            data[self.x],
            data[self.y],
        )

        if self.title is not None:
            axis.set_title(self.title)

        if self.xlabel is not None:
            axis.set_xlabel(self.xlabel)

        if self.ylabel is not None:
            axis.set_ylabel(self.ylabel)

        figure.tight_layout()

        return figure