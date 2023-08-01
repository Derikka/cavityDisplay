# from PyQt5.QtWidgets import QApplication, QMainWindow
# import sys
# from PyQt.QtChart import QChart
import datetime
import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout
from pydm import Display

from lcls_tools.common.data_analysis.archiver import Archiver


class BarChart(Display):
    def __init__(self, parent=None, args=None):
        super(BarChart, self).__init__(parent=parent, args=args,
                                       ui_filename="testBarChart.ui")

        vertLayout_Form = self.ui.findChild(QVBoxLayout)

        # Read in archive data
        pv_strings = ["PPS:SYSW:1:BeamReadyA", "PPS:SYSW:1:BeamReadyB",
                      "ACCL:L2B:1310:SSA_LTCH", "ACCL:L2B:1310:CRYO_LTCH"]
        currentTime = datetime.datetime.now()
        startTime = currentTime - datetime.timedelta(minutes=4 * 24 * 60)
        result = Archiver('lcls').getValuesOverTimeRange(pv_strings, startTime,
                                                         currentTime)
        archive_values_dict = result.values
        print(archive_values_dict)

        # Hard coding interpretting the archive data result
        yaxis_fault = []
        for string, value_list in archive_values_dict.items():
            if string == "PPS:SYSW:1:BeamReadyA":
                # fault status isOkay if value = 1
                fault_counter = 0
                for value in value_list:
                    if value != 1:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(string, value_list, fault_counter)

            elif string == "PPS:SYSW:1:BeamReadyB":
                # fault status isOkay if value = 1
                fault_counter = 0
                for value in value_list:
                    if value != 1:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(string, value_list, fault_counter)

            elif string == "ACCL:L2B:1310:SSA_LTCH":
                # fault status isOkay if value = 0
                fault_counter = 0
                for value in value_list:
                    if value != 0:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(string, value_list, fault_counter)

            elif string == "ACCL:L2B:1310:CRYO_LTCH":
                # fault status isOkay if value = 0
                fault_counter = 0
                for value in value_list:
                    if value != 0:
                        fault_counter += 1
                yaxis_fault.append(fault_counter)
                print(string, value_list, fault_counter)

        print(yaxis_fault)

        # Make plot window and it to the vert layout
        plot_window = pg.plot()
        vertLayout_Form.addWidget(plot_window)

        # Create list for horizontal and vertical axis
        xlabel = ['PPS', 'PPS', 'SSP', 'CSI']
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
        pv_list = Tester().pvList  # ["BEND:LTUH:220:BDES", "BEND:LTUH:280:BDES"]
        start_time = datetime(2020, 10, 1, 10, 7, 28, 958256)  # 220
        end_time = datetime(2020, 10, 14, 9, 57, 57, 230327)  # 220
        result = Archiver('lcls').getValuesOverTimeRange(pvList=pv_list,
                                                         startTime=start_time,
                                                         endTime=end_time)
        print(result)
        '''
