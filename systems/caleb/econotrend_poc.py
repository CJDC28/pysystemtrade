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

    def region(self, instrument_code) -> str:
        region = self.parent.data.get_instrument_region(instrument_code)
        print(f"Region for {instrument_code}: {region}")
        return region


def economic_trend(data, asset_class, instr_reg, rule_region, bullish, bearish):
    """
    Economic trend trading rule
    # Ags, Bond, Equity, FX, Metals, OilGas, STIR, Vol
    """
    region_match = instr_reg == rule_region
    if region_match and (asset_class in bullish):
        result = data
    elif region_match and (asset_class in bearish):
        result = -data
    else:
        result = pd.Series(0.0, index=data.index)

    return result


# US Economic trend rule variation - Growth
us_growth_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class', 'rawdata.region'],
        other_args=dict(
            _trend_name='US_GROWTH',
            rule_region='US',
            bullish=['Equity', 'Ags', 'FX', 'Metals', 'OilGas'],
            bearish=['Bond', 'STIR'],
        )
    )
)

# US Economic trend rule variation - Inflation
us_inflation_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class', 'rawdata.region'],
        other_args=dict(
            _trend_name='US_INFLATION',
            rule_region='US',
            bullish=['Ags', 'FX', 'Metals', 'OilGas'],
            bearish=['Equity', 'Bond', 'STIR'],
        )
    )
)

# US Economic trend rule variation - International Trade
us_inttrade_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class', 'rawdata.region'],
        other_args=dict(
            _trend_name='US_INTTRADE',
            rule_region='US',
            bullish=['Equity'],
            bearish=[],
        )
    )
)

# US Economic trend rule variation - Monetary Policy
us_monpolicy_rule = TradingRule(
    dict(
        function=economic_trend,
        data=['rawdata.economic_trend', 'rawdata.asset_class', 'rawdata.region'],
        other_args=dict(
            _trend_name='US_MONPOLICY',
            rule_region='US',
            bullish=['Equity', 'Ags', 'FX', 'Metals', 'OilGas'],
            bearish=['Bond', 'STIR'],
        )
    )
)

rules = Rules(
    dict(
        etrend_growth=us_growth_rule,
        etrend_inflation=us_inflation_rule,
        etrend_inttrade=us_inttrade_rule,
        etrend_monpolicy=us_monpolicy_rule,
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

    non_us_fc = system.rules.get_raw_forecast("DAX", "etrend_inflation")[-1]
    print(f"non_us_fc forecast: {non_us_fc}")
