from datetime import datetime

from syscore.fileutils import resolve_path_and_filename_for_package

from sysdata.config.production_config import Config
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.diagoutput import systemDiag
from matplotlib.pyplot import show

SAVED_SYSTEM = "systems.caleb.saved-system.pck"

def static_system():
    from systems.provided.futures_chapter15.basesystem import futures_system

    system = futures_system(
        data=dbFuturesSimData(), config=Config("systems.caleb.simple_config.yaml")
    )
    return system


def do_system():
    from sysproduction.strategy_code.run_dynamic_optimised_system import futures_system
    from systems.provided.rob_system.run_system import futures_system

    system = futures_system(
        # data=dbFuturesSimData(),
        # data=csvFuturesSimData(),
        # config=Config("systems.caleb.estimate_config.yaml")
        # config=Config("systems.caleb.simple_config.yaml")
        # config=Config("systems.caleb.andy_strategy_v1.yaml")
        # config_filename="systems.caleb.caleb_strategy_v2.yaml"
        # config_filename="systems.caleb.simple_strategy.yaml"
        config_filename="systems.caleb.caleb_strategy_v3.yaml"
    )
    return system


def write_config(system):
    now = datetime.now()
    sysdiag = systemDiag(system)
    output_file = resolve_path_and_filename_for_package(
        f"systems.caleb.estimate-{now.strftime('%Y-%m-%d_%H%M%S')}.yaml"
    )
    print(f"writing estimate params to: {output_file}")
    sysdiag.yaml_config_with_estimated_parameters(
        output_file,
        [
            #"forecast_scalars",
            #"forecast_weights",
            "forecast_div_multiplier",
            #"instrument_weights",
            #"forecast_mapping",
            #"instrument_div_multiplier",
        ],
    )


def run_dynamic():
    system = do_system()
    portfolio = system.accounts.optimised_portfolio()
    print(portfolio.percent.stats())
    curve = portfolio.curve()

    # filename = f"{PYSYS_CODE}/data/saved_backtests/backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    # curve.to_csv(
    #     filename, index_label="Date"
    # )

    portfolio.curve().plot()
    write_config(system)
    write_pickle_file(system)
    show()


def write_pickle_file(system):
    print(f"Writing pickled system to {SAVED_SYSTEM}")
    system.cache.pickle(SAVED_SYSTEM)


if __name__ == "__main__":
    # static_system()
    run_dynamic()
