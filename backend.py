from datetime import datetime, timedelta
from time import sleep

from display_linac import DISPLAY_MACHINE, DisplayCryomodule
from lcls_tools.common.controls.pyepics.utils import PV
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES
from utils import BACKEND_SLEEP_TIME, DEBUG

WATCHER_PV: PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")
WATCHER_PV.put(0)

while True:
    start = datetime.now()
    for cryomoduleName in ALL_CRYOMODULES:
        cryomodule: DisplayCryomodule = DISPLAY_MACHINE.cryomodules[cryomoduleName]
        for cavity in cryomodule.cavities.values():
            # EX: cavity = L0B CM01 Cavity 2
            # EX: cryomodule.cavities.values() = dict of 8 display_linac.DisplayCavity object
            ########### cavity.run_through_faults() ####PUT THIS BACK IN
            if (cavity.pv_prefix == "ACCL:L1B:H220:"):
                print(cavity.pv_prefix)
                cavity.get_fault_counts(datetime.now() - timedelta(minutes=1), datetime.now())
            # print("Start: ", datetime.now() - timedelta(minutes=1), "End: ", datetime.now())
    if DEBUG:
        delta = (datetime.now() - start).total_seconds()
        sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)

    try:
        WATCHER_PV.put(WATCHER_PV.get() + 1)
    except TypeError as e:
        print(f"Write to watcher PV failed with error: {e}")
