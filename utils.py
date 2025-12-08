import pandas as pd
import numpy as np
import plotly.express as px
from pandas import DataFrame
from scipy.stats import chi2_contingency, pearsonr


class ChiSquareTest:
    def __init__(self, df1: DataFrame, df2: DataFrame) -> None:
        self.contingency_table: DataFrame = pd.crosstab(df1, df2)

        chi_result = chi2_contingency(self.contingency_table)
        stat: float = chi_result.statistic
        self.pvalue: float = chi_result.pvalue

        n: int = self.contingency_table.sum().sum()
        min_dimension: int = min(self.contingency_table.shape) - 1
        self.crammers_v: float = np.sqrt(stat / n / min_dimension)


class PearsonTest:
    def __init__(self, df: DataFrame) -> None:
        correlation = df.corr(method="pearson")
        self.figure = px.imshow(correlation, text_auto=".3f")
