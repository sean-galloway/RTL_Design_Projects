from dataclasses import dataclass
from verilog.verilog_parser import ParserHelper
from typing import Tuple


@dataclass
class ParameterRecord:
    ''' DataClass for the Parameters that could be on a parsed module'''
    sig_type: str
    name: str
    value: str
    packed: str
    unpacked: str
    compilerDirectiveSig: str
    compilerDirective: str


class Param(object):
    '''The class maintains a list of parameter records and performs all of the basic operations on them'''

    def __init__(self, signal_str=''):
        self.paramrec_list: list(ParameterRecord) = []
        if len(signal_str) > 0:
            paramrec_list = ParserHelper.parseParametersList(signal_str)
            self._convert_paramrec_list(paramrec_list)


    def __repr__(self):
        return self.paramrec_list


    def _found_name(self, name: str) -> Tuple[bool, int]:  # sourcery skip: use-next
        for idx, paramrec in enumerate(self.paramrec_list):
            if paramrec.name == name:
                return True, idx
        return False, -1


    def _convert_paramrec_list(self, rec_list):
        for rec in rec_list:
            paramrec = Param._convert_paramrec(rec)
            found, idx = self._found_name(paramrec.name)
            if found:
                current = self.paramrec_list[idx]
                packed_merge = ParserHelper.arrayMerge(current.packed, paramrec.packed)
                unpacked_merge = ParserHelper.arrayMerge(current.unpacked, paramrec.unpacked)
                current.packed = packed_merge
                current.unpacked = unpacked_merge
            else:
                self.paramrec_list.append(paramrec)


    @staticmethod
    def _convert_paramrec(rec) -> ParameterRecord:
        return ParameterRecord(rec['type'],
                            rec['name'],
                            rec['value'],
                            rec['packed'],
                            rec['unpacked'],
                            rec['compilerDirectiveSig'],
                            rec['compilerDirective'])


    def add_param_string(self, signal_str):
        paramrec_list = ParserHelper.parsePortsList(signal_str)
        self._convert_paramrec_list(paramrec_list)
        return self.paramrec_list


    def create_param_string(self) -> str:
        longest_type = 0
        for paramrec in [self.paramrec_list]:  # Iterate through the list
            if len(paramrec.type) > longest_type:
                longest_type = len(paramrec.type)

        comma = ','
        ports = ''
        last = len(self.paramrec_list)
        for idx, paramrec in enumerate(self.paramrec_list):
            sig_type = paramrec.type
            if len(paramrec.type) < longest_type:
                sig_type += ' ' * (longest_type - len(sig_type))
            if idx == last -1:
                comma = ''
            ports += f'{paramrec.direction} {sig_type} {paramrec.packed} {paramrec.name} {paramrec.unpacked} {comma}\n'

        return ports
            