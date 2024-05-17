# from PyQt5.QtWidgets import QApplication, QMainWindow
# import sys
# from PyQt.QtChart import QChart
import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout
from datetime import datetime
from pydm import Display

from lcls_tools.common.data_analysis.archiver import (
    get_values_over_time_range,
)

# from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES

'''
print(ALL_CRYOMODULES)
for cm in ALL_CRYOMODULES:
    print("cm: ", cm)
    cm_obj: DisplayCryomodule = DISPLAY_CRYOMODULES[cm]
    for cav in cm_obj.cavities.values():
        initialTime = datetime.now()
        fault_count_dict = cav.get_fault_counts(starttime=datetime.now() -
                                                          timedelta(minutes=1),
                                                endtime=datetime.now())
        print(cav, datetime.now() - initialTime)
'''


class BarChart(Display):
    def __init__(self, parent=None, args=None):
        super(BarChart, self).__init__(parent=parent, args=args,
                                       ui_filename="testBarChart.ui")

        vertLayout_Form = self.ui.findChild(QVBoxLayout)

        # Read in archive data
        # pv_strings = ["PPS:SYSW:1:BeamReadyA", "ACCL:L3B:1910:PZT:FBSTATSUM",
        #              "ACCL:L2B:1310:SSA_LTCH", "ACCL:L2B:1310:CRYO_LTCH"]

        pv_string = "ACCL:L3B:1910:PZT:FBSTATSUM"
        pv_list = [pv_string]

        start = datetime(2024, 5, 17, 4, 29, 35, 24214)
        end = datetime(2024, 5, 17, 4, 30, 35, 24214)

        # get_values_over_time_range(...) -> Dict[str, ArchiveDataHandler]
        result = get_values_over_time_range(pv_list, start_time=start,
                                            end_time=end)

        data_handler: ArchiveDataHandler = result[pv_string]

        fault_count = 0
        for archiver_value in data_handler.value_list: \
                # Per spreadsheet, PZT:FBSTATSUM faulted if value equal to 1
            if archiver_value.val == 1:
                fault_count += 1
        print(pv_string, "\tTotal fault counts: ", fault_count)

        # Hard coding interpretting the archive data result
        yaxis_fault = []
        yaxis_fault.append(fault_count)

        # Make plot window and it to the vert layout
        plot_window = pg.plot()
        vertLayout_Form.addWidget(plot_window)

        # Create list for horizontal and vertical axis
        xlabel = ['PZO']
        xval = [0]
        # y1 = [5, 10, 1, 0]

        # Create list of list of tuples for tick marks in the form of
        # [[(0,'HWI'), (1,'AOT'), ...]]
        ticks = []
        for i, xlabel_string in enumerate(xlabel):
            ticks.append((xval[i], xlabel_string))
        ticks = [ticks]

        # Create pyqt5graph bar graph item with green bars
        bargraph = pg.BarGraphItem(x=xval, height=yaxis_fault, width=0.6, brush='g')

        ax = plot_window.getAxis('bottom')
        ax.setTicks(ticks)
        plot_window.showGrid(x=False, y=True, alpha=0.6)

        # Add bargraph to plot window
        plot_window.addItem(bargraph)

        '''
        # Hard coding interpretting the archive data result
        yaxis_fault = []
        for pv_string, value_list in archive_values_dict.items():
            if pv_string == "PPS:SYSW:1:BeamReadyA":
                # fault status isOkay if value = 1
                fault_counter = 0
                for value in value_list:
                    if value != 1:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(pv_string, value_list, fault_counter)

            elif pv_string == "ACCL:L3B:1910:PZT:FBSTATSUM":
                # fault status isOkay if value = 1
                fault_counter = 0
                for value in value_list:
                    if value != 1:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(pv_string, value_list, fault_counter)

            elif pv_string == "ACCL:L2B:1310:SSA_LTCH":
                # fault status isOkay if value = 0
                fault_counter = 0
                for value in value_list:
                    if value != 0:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(pv_string, value_list, fault_counter)

            elif pv_string == "ACCL:L2B:1310:CRYO_LTCH":
                # fault status isOkay if value = 0
                fault_counter = 0
                for value in value_list:
                    if value != 0:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(pv_string, value_list, fault_counter)

        print(yaxis_fault)

        # Make plot window and it to the vert layout
        plot_window = pg.plot()
        vertLayout_Form.addWidget(plot_window)

        # Create list for horizontal and vertical axis
        xlabel = ['PPS', 'PZT', 'SSP', 'CSI']
        xval = [0, 1, 2, 3]
        # y1 = [5, 10, 1, 0]

        # Create list of list of tuples for tick marks in the form of
        # [[(0,'HWI'), (1,'AOT'), ...]]
        ticks = []
        for i, xlabel_string in enumerate(xlabel):
            ticks.append((xval[i], xlabel_string))
        ticks = [ticks]

        # Create pyqt5graph bar graph item with green bars
        bargraph = pg.BarGraphItem(x=xval, height=yaxis_fault, width=0.6, brush='g')

        ax = plot_window.getAxis('bottom')
        ax.setTicks(ticks)
        plot_window.showGrid(x=False, y=True, alpha=0.6)

        # Add bargraph to plot window
        plot_window.addItem(bargraph)

        '''
        '''
        pv_list = Tester().pvList  # ["BEND:LTUH:220:BDES", "BEND:LTUH:280:BDES"]
        start_time = datetime(2020, 10, 1, 10, 7, 28, 958256)  # 220
        end_time = datetime(2020, 10, 14, 9, 57, 57, 230327)  # 220
        result = Archiver('lcls').getValuesOverTimeRange(pvList=pv_list,
                                                         startTime=start_time,
                                                         endTime=end_time)
        print(result)
        '''
