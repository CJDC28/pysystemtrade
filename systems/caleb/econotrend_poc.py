import pandas as pd
from systems.provided.futures_chapter15.basesystem import *
from systems.trading_rules import TradingRule
from sysdata.csv.csv_economic_data import csvEconomicTrendData

data = csvFuturesSimData()
data.data.add_class_object(csvEconomicTrendData)
config = Config("systems.caleb.economic_trend_poc.yaml")


class calebRawData(RawData):
    """
    custom raw data class
    """
    def economic_trend(self, instrument_code, trend_name) -> pd.Series:
        df = self.data_stage.data.db_economic_trend.get_trend(trend_name)
        series = df["ewmac"]
        print(f"Economic trend {trend_name}:\n{series}")
        return series

    def asset_class(self, instrument_code) -> str:
        asset_class = self.parent.data.asset_class_for_instrument(instrument_code)
        print(f"Asset class for {instrument_code}: {asset_class}")
        return asset_class


def economic_trend(data, asset_class, bullish, bearish):
    """
    Economic trend trading rule
    # Ags, Bond, Equity, FX, Metals, OilGas, STIR, Vol
    """
    if asset_class in bullish:
        result = data
    elif asset_class in bearish:
        result = -data
    else:
        result = data[:] = 0

    return result


# Economic trend rule variation - Growth
growth_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class'],
        other_args=dict(
            _trend_name='GROWTH',
            bullish=['Equity', 'Ags', 'FX', 'Metals', 'OilGas'],
            bearish=['Bond', 'STIR'],
        )
    )
)

# Economic trend rule variation - Inflation
inflation_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class'],
        other_args=dict(
            _trend_name='INFLATION',
            bullish=['FX'],
            bearish=['Equity', 'Bond', 'STIR'],
        )
    )
)

# Economic trend rule variation - International Trade
inttrade_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class'],
        other_args=dict(
            _trend_name='INTTRADE',
            bullish=['Equity'],
            bearish=[],
        )
    )
)

# Economic trend rule variation - Monetary Policy
monpolicy_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class'],
        other_args=dict(
            _trend_name='MONPOLICY',
            bullish=['Equity', 'Ags', 'FX', 'Metals', 'OilGas'],
            bearish=['Bond', 'STIR'],
        )
    )
)

rules = Rules(
    dict(
        etrend_growth=growth_rule,
        etrend_inflation=inflation_rule,
        etrend_inttrade=inttrade_rule,
        etrend_monpolicy=monpolicy_rule,
    )
)

system = System([
   Account(), Portfolios(), PositionSizing(), calebRawData(),
   ForecastCombine(), ForecastScaleCap(), rules
], data, config)


if __name__ == "__main__":
    growth_fc = system.rules.get_raw_forecast("SP500", "etrend_growth")[-1]
    print(f"growth forecast: {growth_fc}")

    inflation_fc = system.rules.get_raw_forecast("SP500", "etrend_inflation")[-1]
    print(f"inflation forecast: {inflation_fc}")
