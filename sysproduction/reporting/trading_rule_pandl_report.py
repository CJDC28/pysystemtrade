import datetime
import pandas as pd
from syscore.constants import arg_not_supplied
from syscore.dateutils import get_date_from_period_and_end_date
from sysdata.data_blob import dataBlob
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from sysproduction.reporting.formatting import make_account_curve_plot_from_df
from sysproduction.reporting.reporting_functions import (
    PdfOutputWithTempFileName,
)
from systems.provided.rob_system.run_system import futures_system, System


def trading_rule_pandl_report(
    data: dataBlob = arg_not_supplied,
    dict_of_rule_groups: dict = None,
    list_of_periods: list = None,
    system_function: System = None,
    config_filename: str = None,
):
    if data is arg_not_supplied:
        data = dataBlob()

    if config_filename is None:
        config_filename = "systems.caleb.caleb_strategy_v3.yaml"

    if system_function is None:
        sim_data = dbFuturesSimData(csv_data_paths=data.csv_data_paths)
        system_function = futures_system(
            sim_data=sim_data,
            config_filename=config_filename,
        )

    if list_of_periods is None:
        list_of_periods = ["YTD", "1Y", "3Y", "10Y", "99Y"]
    list_of_rule_groups = list(dict_of_rule_groups.keys())

    report_output = []

    for rule_group in list_of_rule_groups:
        # We reload to avoid memory blowing up
        system_function.get_instrument_list(
            remove_duplicates=True,
            remove_ignored=True,
            remove_trading_restrictions=True,
            remove_bad_markets=True,
        )

        for period in list_of_periods:
            start_date = get_date_from_period_and_end_date(period)

            figure_object = get_figure_for_rule_group(
                rule_group=rule_group,
                dict_of_rule_groups=dict_of_rule_groups,
                data=data,
                system=system_function,
                start_date=start_date,
                period_label=period,
            )

            report_output.append(figure_object)

    return report_output


def get_figure_for_rule_group(
    rule_group: str,
    data: dataBlob,
    system: System,
    dict_of_rule_groups: dict,
    start_date: datetime.datetime,
    period_label: str,
):
    rules = dict_of_rule_groups[rule_group]
    pandl_by_rule = dict(
        [
            (rule_name, system.accounts.pandl_for_trading_rule(rule_name).percent.as_ts)
            for rule_name in rules
        ]
    )
    concat_pd_by_rule = pd.concat(pandl_by_rule, axis=1)
    concat_pd_by_rule.columns = rules

    pdf_output = PdfOutputWithTempFileName(data)
    make_account_curve_plot_from_df(
        concat_pd_by_rule,
        start_of_title=f"Total Trading Rule P&L for period '{period_label}'",
        start_date=start_date,
        title_style={"size": 6},
    )

    figure_object = pdf_output.save_chart_close_and_return_figure()

    return figure_object
