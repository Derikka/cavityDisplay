# from PyQt5.QtWidgets import QApplication, QMainWindow
# import sys
# from PyQt.QtChart import
import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout, QApplication
from datetime import datetime
from pydm import Display

from lcls_tools.common.data_analysis.archiver import (
    get_values_over_time_range,
)


class BarChart(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(parent, args)

        print("TEST: this is bar_chart_display.py")

        pv_string1 = "ACCL:L3B:1910:PZT:FBSTATSUM"  # PZO fault
        pv_string2 = "XCOR:L3B:1685:STATMSG"  # MGT fault
        pv_list = [pv_string1, pv_string2]

        start = datetime(2024, 5, 17, 4, 29, 35, 24214)
        end = datetime(2024, 5, 17, 4, 30, 35, 24214)

        # get_values_over_time_range(...) -> Dict[str, ArchiveDataHandler]
        result = get_values_over_time_range(pv_list, start_time=start,
                                            end_time=end)

        # Hard coding interpretting the archive data result
        yaxis_fault = []
        for key, value in result.items():
            data_handler: ArchiveDataHandler = result[key]

            if key == pv_string1:
                fault_count = 0
                for archiver_value in data_handler.value_list:
                    if archiver_value.val == 1:
                        fault_count += 1
                yaxis_fault.append(fault_count)
                print(key, "\tTotal fault counts: ", fault_count)

            elif key == pv_string2:
                fault_count = 0
                for archiver_value in data_handler.value_list:
                    if archiver_value.val == 8:
                        fault_count += 1
                yaxis_fault.append(fault_count)
                print(key, "\tTotal fault counts: ", fault_count)

        self.setWindowTitle("Bar Chart")
        vertLayout_Form = QVBoxLayout()

        # Make plot window and add it to the vert layout
        self.plot_window = pg.plot()
        vertLayout_Form.addWidget(self.plot_window)

        self.setLayout(vertLayout_Form)

        # Create list for horizontal and vertical axis
        xlabel = ['PZO', 'MGT']
        xval = [0, 1]

        # Create list of list of tuples for tick marks in the form of
        # [[(0,'HWI'), (1,'AOT'), ...]]
        ticks = []
        for i, xlabel_string in enumerate(xlabel):
            ticks.append((xval[i], xlabel_string))
        ticks = [ticks]

        # Create pyqt5graph bar graph item with green bars
        bargraph = pg.BarGraphItem(x=xval, height=yaxis_fault, width=0.6, brush='g')

        ax = self.plot_window.getAxis('bottom')
        ax.setTicks(ticks)
        self.plot_window.showGrid(x=False, y=True, alpha=0.6)

        # Add bargraph to plot window
        self.plot_window.addItem(bargraph)


def main():
    app = QApplication(sys.argv)
    chart = BarChart()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
