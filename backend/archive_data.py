from datetime import datetime, timedelta
from typing import Dict

print("Actual start of archive_data.py before import statements++++++++++++++++++")
from backend.backend_cavity import BackendCavity
from backend.fault import FaultCounter
from bar_chart_display import BarChart
from lcls_tools.superconducting.sc_linac import Machine

DISPLAY_MACHINE = Machine(cavity_class=BackendCavity)

print("Start of archive_data.py file +++++++++++++++++++++++++++++++++++++++++++")
cavity = DISPLAY_MACHINE.cryomodules["H2"].cavities[2]

tlc_list = []
fault_count_list = []

# Ex. result is a dictionary with key=fault pv string, value=FaultCounter(fault_count=0, ok_count=1, invalid_count=0)
result: Dict[str, FaultCounter] = cavity.get_fault_counts(datetime.now() - timedelta(minutes=1),
                                                          datetime.now())
for tlc, counter_obj in result.items():
    tlc_list.append(tlc)  # x axis
    fault_count_list.append(counter_obj.sum_fault_count)  # y axis

    '''
    print(tlc, "\t", counter_obj,
          counter_obj.fault_count,
          counter_obj.ok_count,
          counter_obj.invalid_count)
    '''
print("right before BarChart call in archive_data.py++++++++++++")
BarChart(x_vals=tlc_list, y_vals=fault_count_list)
print("End of archive_data.py++++++++++++++++++++++++++++++++++")
