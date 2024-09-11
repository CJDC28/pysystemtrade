import pickle
from syscore.fileutils import resolve_path_and_filename_for_package
from syscore.interactive.progress_bar import progressBar
from sysdata.data_blob import dataBlob
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysproduction.reporting.reporting_functions import (
    run_report_with_data_blob,
    pandas_display_for_reports,
)
from sysproduction.reporting.data.risk import get_risk_data_for_instrument
from sysproduction.reporting.report_configs import *


"""

>>> from sysproduction.reporting.debug_report import *
>>> run_roll_report()
>>> run_roll_report(instrument_code='GOLD')
>>> run_pandl_report()
>>> run_trade_report()
>>> run_strategy_report()
>>> run_risk_report()
>>> run_status_report()
>>> run_instrument_risk_report()
>>> run_min_capital_report()
>>> run_remove_markets_report()
>>> run_slippage_report()

"""


def do_report(config: reportConfig):
    pandas_display_for_reports()
    with dataBlob(log_name=f"Test {config.title}") as data:
        run_report_with_data_blob(config, data)


def run_slippage_report():
    do_report(slippage_report_config.new_config_with_modified_output("console"))


def run_costs_report():
    pass


def run_roll_report():
    do_report(roll_report_config.new_config_with_modified_output("console"))


def run_daily_pandl_report():
    do_report(daily_pandl_report_config.new_config_with_modified_output("console"))


def run_reconcile_report():
    pass


def run_trade_report():
    do_report(trade_report_config.new_config_with_modified_output("console"))


def run_strategy_report():
    do_report(strategy_report_config.new_config_with_modified_output("console"))


def run_risk_report():
    do_report(risk_report_config.new_config_with_modified_output("console"))


def run_status_report():
    do_report(status_report_config.new_config_with_modified_output("console"))


def run_liquidity_report():
    pass


def run_instrument_risk_report():
    do_report(instrument_risk_report_config.new_config_with_modified_output("console"))


def run_min_capital_report():
    do_report(min_capital_report_config.new_config_with_modified_output("console"))


def run_duplicate_market_report():
    pass


def run_remove_markets_report():
    do_report(remove_markets_report_config.new_config_with_modified_output("console"))


def run_market_monitor_report():
    pass


def run_account_curve_report():
    pass


def run_trading_rule_pandl_report():
    do_report(trading_rule_pandl_report_config.new_config_with_modified_output("file"))


def instrument_risk_csv():
    output = dict()
    sim_data = csvFuturesSimData()
    instr_list = sim_data.db_futures_multiple_prices_data.get_list_of_instruments()
    p = progressBar(len(instr_list))
    for instr in instr_list:
        risk = get_risk_data_for_instrument(sim_data.data, instr)
        output[instr] = risk
        p.iterate()
    p.close()

    filename = resolve_path_and_filename_for_package(
        "sysproduction.reporting", "futures_instrument_risk.pickle"
    )
    with open(filename, "wb+") as fhandle:
        pickle.dump(output, fhandle)


if __name__ == "__main__":
    # run_slippage_report()
    # run_costs_report()
    # run_roll_report()
    # run_daily_pandl_report()
    # run_reconcile_report()
    # run_trade_report()
    run_strategy_report()
    # run_risk_report()
    # run_status_report()
    # run_liquidity_report()
    # run_instrument_risk_report()
    # run_min_capital_report()
    # run_duplicate_market_report()
    # run_remove_markets_report()
    # run_market_monitor_report()
    # run_account_curve_report()
    # run_slippage_report()
    # run_trading_rule_pandl_report()

    # run_fsb_report()
    # run_min_capital_fsb_report()
    # run_instrument_risk_fsb_report()

    # run_adhoc_tradeable_report()
    # run_adhoc_tradeable_report(instr_code="GAS_US_fsb")

    # instrument_risk_csv()
