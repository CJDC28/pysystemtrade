import pandas as pd


class economicTrendData(pd.DataFrame):

    @classmethod
    def create_empty(cls):
        trend_data = economicTrendData(pd.DataFrame())
        return trend_data
