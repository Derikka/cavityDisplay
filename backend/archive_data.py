from backend.backend_cavity import BackendCavity
from bar_chart_display import BarChart
from lcls_tools.superconducting.sc_linac import Machine, Cryomodule
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES

DISPLAY_MACHINE = Machine(cavity_class=BackendCavity)

for cryomoduleName in ALL_CRYOMODULES:
    cryomodule: Cryomodule = DISPLAY_MACHINE.cryomodules[cryomoduleName]
    for cavity in cryomodule.cavities.values():
        if (cavity.pv_prefix == "ACCL:L1B:H220:"):
            print("CM H2, cavity 2")
            BarChart()

'''
while True:
    start = datetime.now()
    for cryomoduleName in ALL_CRYOMODULES:
        cryomodule: Cryomodule = DISPLAY_MACHINE.cryomodules[cryomoduleName]
        for cavity in cryomodule.cavities.values():
            # EX: cavity = L0B CM01 Cavity 2
            # EX: cryomodule.cavities.values() = dict of 8 backend.backend_cavity.BackendCavity objects
            if (cavity.pv_prefix == "ACCL:L1B:H220:"):
                BarChart()
                print("I am here")
                
                result = cavity.get_fault_counts(datetime.now() - timedelta(minutes=1), datetime.now())
                for faultPv in result:
                    print(faultPv, "\t", result[faultPv],
                          result[faultPv].fault_count,
                          result[faultPv].ok_count,
                          result[faultPv].invalid_count)
                print("Start: ", datetime.now() - timedelta(minutes=1), "End: ", datetime.now())
                
        if DEBUG:
            delta = (datetime.now() - start).total_seconds()
            sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)
'''
