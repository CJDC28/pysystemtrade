from sysdata.data_blob import dataBlob
from sysproduction.interactive_controls import auto_update_spread_costs


def update_slippage():
    with dataBlob(
        log_name="Update-Slippage",
    ) as data:
        obj = updateSlippage(data)
        obj.update_slippage()


class updateSlippage(object):
    def __init__(self, data):
        self.data = data
        self.filter_on = 20.0

    def update_slippage(self):
        auto_update_spread_costs(self.data, self.filter_on)


if __name__ == "__main__":
    update_slippage()
