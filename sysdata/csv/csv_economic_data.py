from matplotlib.pyplot import show
import pandas as pd

from sysdata.base_data import baseData
from syscore.constants import arg_not_supplied
from syscore.fileutils import (
    files_with_extension_in_pathname,
)
from syscore.pandas.pdutils import pd_readcsv
from syslogging.logger import *
from sysobjects.economic_trend_data import economicTrendData

ECONOMIC_TREND_DIRECTORY = "data.economic_trend.fred"

# GROWTH has quarterly values from 1948
# MONPOLICY has daily values from mid 2018
# INFLATION has monthly values from mid 2003
# INTTRADE has daily values from 1998, hourly from mid 2008
# RISKAV
trend_config = {
    "US_GROWTH": {
        "span": 4,
        "from_year": 2000,
        "date_format": "%Y-%m-%d",
    },
    "US_MONPOLICY": {
        "span": 64,
        "from_year": 2018,
        "date_format": "%Y-%m-%d",
    },
    "US_INFLATION": {
        "span": 16,
        "from_year": 2003,
        "date_format": "%b %Y",
    },
    "US_INTTRADE": {
        "span": 256,
        "from_year": 2009,
        "date_format": "%Y-%m-%d",
        "multiplier": 0.01,
        "resample": "1B",
    },
    "US_RISKAV": {
        "span": 4,
        "date_format": "%Y-%m-%d",
    },
}


class csvEconomicTrendData(baseData):

    def __init__(
        self, datapath=arg_not_supplied, log=get_logger("csvEconomicTrendData")
    ):
        super().__init__(log=log)

        if datapath is arg_not_supplied:
            datapath = ECONOMIC_TREND_DIRECTORY

        self._datapath = datapath

    def __repr__(self):
        return "csvEconomicTrendData from %s" % self._datapath

    @property
    def datapath(self):
        return self._datapath

    def get_trend_list(self) -> list:
        return files_with_extension_in_pathname(self.datapath, ".csv")

    def is_code_in_data(self, trend_code: str) -> bool:
        return trend_code in self.get_trend_list()

    def get_trend(self, trend_code: str) -> economicTrendData:

        if self.is_code_in_data(trend_code):
            filename = self._filename_given_instrument_code(trend_code)

            config = trend_config[trend_code]

            try:
                df = pd_readcsv(
                    filename,
                    date_format=config["date_format"]
                )
            except OSError:
                self.log.warning("Can't find economic trend file %s" % filename)
                return economicTrendData.create_empty()

            df.columns = ["value"]

            mask = (df.index > datetime.datetime(config["from_year"], 1, 1))
            df = df.loc[mask]

            if "multiplier" in config:
                df["value"] = df["value"] * config["multiplier"]

            if "resample" in config:
                df = df.resample(config["resample"]).last()

            df['fast_ewma'] = pd.Series.ewm(df['value'], span=config["span"]).mean()
            df['slow_ewma'] = pd.Series.ewm(df['value'], span=config["span"]*4).mean()
            df['ewmac'] = df['fast_ewma'] - df['slow_ewma']

            trend_data = economicTrendData(df)

            return trend_data
        else:
            trend_data = economicTrendData.create_empty()

        return trend_data

    def _filename_given_instrument_code(self, trend_code: str):
        return resolve_path_and_filename_for_package(
            self.datapath, f"{trend_code}.csv"
        )


if __name__ == "__main__":
    data = csvEconomicTrendData()
    for trend in ["GROWTH", "MONPOLICY", "INFLATION", "INTTRADE"]:
        df = data.get_trend(trend)
        #df = df["ewmac"]
        df.plot(title=trend)
        show()
