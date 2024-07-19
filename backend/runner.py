from datetime import datetime
from time import sleep

from backend.backend_cavity import BackendCavity
# from bar_chart_test import BarChart
from lcls_tools.common.controls.pyepics.utils import PV
from lcls_tools.superconducting.sc_linac import Machine, Cryomodule
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES
from utils.utils import DEBUG, BACKEND_SLEEP_TIME

WATCHER_PV: PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")
WATCHER_PV.put(0)

DISPLAY_MACHINE = Machine(cavity_class=BackendCavity)

while True:
    start = datetime.now()
    for cryomoduleName in ALL_CRYOMODULES:
        cryomodule: Cryomodule = DISPLAY_MACHINE.cryomodules[cryomoduleName]
        for cavity in cryomodule.cavities.values():
            # EX: cavity = L0B CM01 Cavity 2
            # EX: cryomodule.cavities.values() = dict of 8 backend.backend_cavity.BackendCavity objects
            # cavity.run_through_faults()  ####TODO PUT THIS BACK IN
            if (cavity.pv_prefix == "ACCL:L1B:H220:"):
                # BarChart()
                print("I am here")
                cavity.get_fault_counts(datetime.now() - timedelta(minutes=1), datetime.now())
                print("Start: ", datetime.now() - timedelta(minutes=1), "End: ", datetime.now())
        if DEBUG:
            delta = (datetime.now() - start).total_seconds()
            sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)

        try:
            WATCHER_PV.put(WATCHER_PV.get() + 1)
        except TypeError as e:
            print(f"Write to watcher PV failed with error: {e}")
