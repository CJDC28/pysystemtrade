from copy import copy

from sysobjects.production.roll_state import ALL_ROLL_INSTRUMENTS


class reportConfig(object):
    def __init__(self, title, function, output="console", **kwargs):
        assert output in ["console", "email", "file", "emailfile"]
        self.title = title
        self.function = function
        self.output = output
        self.kwargs = kwargs

    def __repr__(self):
        return "%s %s %s %s" % (
            self.title,
            self.function,
            self.output,
            str(self.kwargs),
        )

    def new_config_with_modified_output(self, output):
        new_config = copy(self)
        new_config.output = output

        return new_config

    def new_config_with_modify_kwargs(self, **kwargs):
        new_config = copy(self)
        new_config.modify_kwargs(**kwargs)

        return new_config

    def modify_kwargs(self, **kwargs):
        for key in kwargs.keys():
            self.kwargs[key] = kwargs[key]

        return self


status_report_config = reportConfig(
    title="Status report",
    function="sysproduction.reporting.status_report.status_report",
    output="email",
)

roll_report_config = reportConfig(
    title="Roll report",
    function="sysproduction.reporting.roll_report.roll_report",
    instrument_code=ALL_ROLL_INSTRUMENTS,
    output="email",
)

daily_pandl_report_config = reportConfig(
    title="P&L report",
    function="sysproduction.reporting.pandl_report.pandl_report",
    calendar_days_back=1,
    output="email",
)

reconcile_report_config = reportConfig(
    title="Reconcile report",
    function="sysproduction.reporting.reconcile_report.reconcile_report",
    output="email",
)

trade_report_config = reportConfig(
    title="Trade report",
    function="sysproduction.reporting.trades_report.trades_report",
    calendar_days_back=1,
    output="email",
)

strategy_report_config = reportConfig(
    title="Strategy report",
    function="sysproduction.reporting.strategies_report.strategy_report",
    output="email",
)

risk_report_config = reportConfig(
    title="Risk report",
    function="sysproduction.reporting.risk_report.risk_report",
    output="email",
)

liquidity_report_config = reportConfig(
    title="Liquidity report",
    function="sysproduction.reporting.liquidity_report.liquidity_report",
    output="email",
)

costs_report_config = reportConfig(
    title="Costs report",
    function="sysproduction.reporting.costs_report.costs_report",
    output="email",
    calendar_days_back=250,
)

slippage_report_config = reportConfig(
    title="Slippage report",
    function="sysproduction.reporting.slippage_report.slippage_report",
    calendar_days_back=250,
    output="email",
)

commission_report_config = reportConfig(
    title="Commission report",
    function="sysproduction.reporting.commissions_report.commissions_report",
    output="email",
)

instrument_risk_report_config = reportConfig(
    title="Instrument risk report",
    function="sysproduction.reporting.instrument_risk_report.instrument_risk_report",
    output="email",
)

min_capital_report_config = reportConfig(
    title="Minimum capital report",
    function="sysproduction.reporting.minimum_capital_report.minimum_capital_report",
    output="email",
)

duplicate_market_report_config = reportConfig(
    title="Duplicate markets report",
    function="sysproduction.reporting.duplicate_market_report.duplicate_market_report",
    output="email",
)

remove_markets_report_config = reportConfig(
    title="Remove markets report",
    function="sysproduction.reporting.remove_markets_report.remove_markets_report",
    output="email",
)

market_monitor_report_config = reportConfig(
    title="Market monitor report",
    function="sysproduction.reporting.market_monitor_report.market_monitor_report",
    output="email",
)

account_curve_report_config = reportConfig(
    title="Account curve report",
    function="sysproduction.reporting.account_curve_report.account_curve_report",
    output="email",
)

trading_rule_pandl_report_config = reportConfig(
    title="Trading Rule P&L report",
    function="sysproduction.reporting.trading_rule_pandl_report.trading_rule_pandl_report",
    output="email",
    config_filename="systems.caleb.caleb_strategy_v3.yaml",
    #config_filename="systems.caleb.caleb_strategy_v3_debug.yaml",
    dict_of_rule_groups=dict(
        acceleration=["accel16", "accel32", "accel64"],
        asset_class_trend=[
            "assettrend2",
            "assettrend4",
            "assettrend8",
            "assettrend16",
            "assettrend32",
            "assettrend64",
        ],
        breakout=[
            "breakout10",
            "breakout20",
            "breakout40",
            "breakout80",
            "breakout160",
            "breakout320",
        ],
        ewmac_momentum=[
            "momentum4",
            "momentum8",
            "momentum16",
            "momentum32",
            "momentum64",
        ],
        normalised_momentum=[
            "normmom2",
            "normmom4",
            "normmom8",
            "normmom16",
            "normmom32",
            "normmom64",
        ],
        relative_momentum=[
            "relmomentum10",
            "relmomentum20",
            "relmomentum40",
            "relmomentum80",
        ],
        carry=["carry10", "carry30", "carry60", "carry125"],
        relative_carry=["relcarry"],
        skew=['skewabs180', 'skewabs365', 'skewrv180', 'skewrv365'],
        misc_mr=["mrinasset1000"],
    ),
    # dict_of_rule_groups=dict(
    #     ewmac_momentum=["momentum8", "momentum32"],
    #     carry=["carry30", "carry60"],
    # ),
    #list_of_periods=["YTD", "1Y", "3Y", "10Y", "99Y"],
    list_of_periods=["1Y", "3Y", "10Y", "99Y"],
)


## The reports will be run in this order
report_config_defaults = dict(
    slippage_report=slippage_report_config,
    costs_report=costs_report_config,
    roll_report=roll_report_config,
    daily_pandl_report=daily_pandl_report_config,
    reconcile_report=reconcile_report_config,
    trade_report=trade_report_config,
    strategy_report=strategy_report_config,
    risk_report=risk_report_config,
    status_report=status_report_config,
    liquidity_report=liquidity_report_config,
    instrument_risk_report=instrument_risk_report_config,
    min_capital=min_capital_report_config,
    duplicate_market=duplicate_market_report_config,
    remove_markets_report=remove_markets_report_config,
    market_monitor_report=market_monitor_report_config,
    account_curve_report=account_curve_report_config,
    commission_report=commission_report_config,
    trading_rule_pandl_report=trading_rule_pandl_report_config,
)
