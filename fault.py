from typing import List, Optional

from lcls_tools.common.data_analysis.archiver import ArchiverData
from lcls_tools.common.pyepics_tools.pyepics_utils import PV
from utils import ARCHIVER

PV_TIMEOUT = 0.01


class PvInvalid(Exception):
    def __init__(self, message):
        super(PvInvalid, self).__init__(message)


class Fault:
    def __init__(self, tlc, severity, pv, okValue, faultValue, longDescription,
                 shortDescription, button_level, button_command, macros,
                 button_text, button_macro):
        self.tlc = tlc
        self.severity = int(severity)
        self.longDescription = longDescription
        self.shortDescription = shortDescription
        self.okValue = float(okValue) if okValue else None
        self.faultValue = float(faultValue) if faultValue else None
        self.button_level = button_level
        self.button_command = button_command
        self.macros = macros
        self.button_text = button_text
        self.button_macro = button_macro

        self.pv_str: str = pv
        self._pv_obj: Optional[PV] = None

    @property
    def pv_obj(self):
        if not self._pv_obj:
            self._pv_obj = PV(self.pv_str)
        return self._pv_obj

    def get_fault_count(self, startime, endtime):
        data: ArchiverData = ARCHIVER.getValuesOverTimeRange([self.pv_str],
                                                             startTime=startime,
                                                             endTime=endtime)
        values: List = data.values[self.pv_str]
        counter = 0

        for value in values:
            if self.value_is_faulted(value):
                counter += 1

        return counter

    def value_is_faulted(self, value) -> bool:
        if self.okValue is not None:
            return value != self.okValue

        elif self.faultValue is not None:
            return value == self.faultValue

        else:
            print(self)
            raise Exception("Fault has neither \'Fault if equal to\' nor"
                            " \'OK if equal to\' parameter")

    def is_realtime_faulted(self) -> bool:
        """
        Dug through the pyepics source code to find the severity values:
        class AlarmSeverity(DefaultIntEnum):
            NO_ALARM = 0
            MINOR = 1
            MAJOR = 2
            INVALID = 3
        """
        if self.pv_obj.severity == 3 or self.pv_obj.status is None:
            raise PvInvalid(self.pv_obj.pvname)

        return self.value_is_faulted(self.pv_obj.value)
