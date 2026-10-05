from dataclasses import dataclass

import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .base import Chart

@dataclass(slots=True)
class PieChart(Chart):
    labels: str
    values: str
    title: str | None = None

    def render(self, data: pd.DataFrame) -> Figure:
        figure, axis = plt.subplots()

        axis.pie(
            data[self.values],
            labels=data[self.labels],
            autopct="%1.1f%%",
        )

        if self.title is not None:
            axis.set_title(self.title)

        return figure