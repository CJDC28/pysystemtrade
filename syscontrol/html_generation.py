import shutil
from jinja2 import Environment, select_autoescape, FileSystemLoader

from sysdata.data_blob import dataBlob
from sysdata.config.production_config import get_production_config
from syslogging.logger import *


def build_dashboard(data: dataBlob, context: dict):
    data.log.info(f"Starting build of monitor page with context: {context.keys()} ...")
    jinja = _get_env()
    template = jinja.get_template("monitor.html")
    with open(get_html_file_path(), "w") as file:
        file.write(template.render(context))
    data.log.info("monitor build complete")


def build_reports(data: dataBlob, context: dict):
    data.log.info(f"Starting build of site reports with context: {context.keys()} ...")
    jinja = _get_env()
    template = jinja.get_template("report_template.html")
    report_list = [
        "Commission_report.txt",
        "Costs_report.txt",
        "Duplicate_markets_report.txt",
        "Instrument_risk_report.txt",
        "Liquidity_report.txt",
        "Market_monitor_report.txt",
        "Minimum_capital_report.txt",
        "P&L_report.txt",
        "Reconcile_report.txt",
        "Remove_markets_report.txt",
        "Risk_report.txt",
        "Roll_report.txt",
        "Slippage_report.txt",
        "Status_report.txt",
        "Strategy_report.txt",
        "Trade_report.txt",
    ]
    for report in report_list:
        with open(get_site_report_file_path(report), "w") as file:
            data.log.info(f"Generating HTML wrapper for {report}")
            file.write(template.render({"filename": report}))
    pdf_report_list = [
        "Account_curve_report.txt.pdf",
        "Trading_Rule_P&L.txt.pdf",
    ]
    config = get_production_config()
    rep_dir = config.get_element("reporting_directory")
    site_rep_dir = config.get_element("site_report_path")
    for report in pdf_report_list:
        data.log.info(f"Copying PDF file {report}")
        shutil.copy(f"{rep_dir}/{report}", site_rep_dir)

    data.log.info("Site reports build complete")


def get_html_file_path():
    path = get_production_config().get_element_or_default(
        "monitor_output_path", "private.index.html"
    )
    resolved_path = resolve_path_and_filename_for_package(path)
    return resolved_path


def get_site_report_file_path(filename):
    path = get_production_config().get_element_or_default(
        "site_report_path", "private.report.html"
    )
    html_file = os.path.splitext(filename)[0] + ".html"
    resolved_path = resolve_path_and_filename_for_package(path, html_file)
    return resolved_path


def _get_env():
    templates = get_production_config().get_element("site_templates")
    jinja = Environment(
        loader=FileSystemLoader(templates),
        autoescape=select_autoescape(),
    )
    return jinja


if __name__ == "__main__":
    build_dashboard({})
