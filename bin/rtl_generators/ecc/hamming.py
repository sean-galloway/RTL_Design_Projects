from rtl_generators.verilog.module import Module


class Hamming(Module):
    module_str = 'dataint_ecc_hamming'
    param_str = 'parameter int N=8, parameter int ECC=3'


    def __init__(self, buswidth):
        Module.__init__(self, module_name=self.module_str)
        self.ports.add_port_string(self.port_str)
        self.params.add_param_string(self.param_str)
        self.buswidth = buswidth
        ecc_bits = 1
        while (1 << ecc_bits) - ecc_bits - 1 < buswidth:
            ecc_bits += 1
        self.ecc_bits = ecc_bits
        self.total_bits = ecc_bits + buswidth
        self.module_name = f'{self.module_name}_{str(self.buswidth).zfill(3)}'
        self.params.set_param_value('N', self.buswidth)
        self.params.set_param_value('ECC', self.ecc_bits)
        self.matrix = [0] * (self.total_bits)
        self.syndrome = [0] * (self.total_bits+1)
        self.__generate_syndrome_list()


    def __generate_syndrome_list(self):
        j = 1
        for i in range(self.total_bits):
            self.matrix[i] = j
            self.syndrome[j] = 1
            if i < self.ecc_bits - 1:
                j = j << 1  # Left shift j by 1
            elif i == self.ecc_bits - 1:
                j = 3     # this looks fishy to me... TODO: fix this
            elif i < self.total_bits - 1:
                while True:
                    j += 1
                    if not self.syndrome[j]:
                        break


class HammingEncode(Hamming):
    module_str = 'dataint_ecc_hamming_encode'
    port_str = '''
    input   logic [N-1:0]   i_data,
    output  logic [ECC-1:0] o_ecc
    '''


    def __init__(self, buswidth):
        super().__init__(buswidth)
        # self.module_name = f'{self.module_name}_{str(self.buswidth).zfill(3)}'


    def generate_ecc(self):
        self.comment('Hamming ECC Generation')
        for i in range(self.ecc_bits):
            start = False
            ecc_line = f'assign o_ecc[{i}] = '
            for j in range(self.ecc_bits, self.total_bits):
                if self.matrix[j] & (1 << i):
                    if start is True:
                        ecc_line += ' ^ '
                    ecc_line += f'i_data[{self.total_bits-j-1}]'
                    start = True
            ecc_line += ';'
            self.instruction(ecc_line)


    def verilog(self, file_path):  # sourcery skip: extract-duplicate-method
        self.comment('Generated by the Hamming Class; do not modify the code')
        self.generate_ecc()
        self.instruction('')
        self.instruction('// synopsys translate_off')
        self.instruction('initial begin')
        self.instruction('    $dumpfile("dump.vcd");')
        self.instruction(f'    $dumpvars(0, {self.module_name});')
        self.instruction('end')
        self.instruction('// synopsys translate_on')
        self.instruction('')
        self.start()
        self.end()
        self.write(file_path, f'{self.module_name}.sv')


class HammingDecode(Hamming):
    module_str = 'dataint_ecc_hamming_decode'
    port_str = '''
    input   logic [N-1:0]   i_data,
    input   logic [ECC-1:0] i_ecc,
    output  logic [N-1:0]   o_data,
    output  logic           o_error,
    output  logic           o_repairable
    '''


    def __init__(self, buswidth):
        super().__init__(buswidth)
        # self.module_name = f'{self.module_name}_{str(self.buswidth).zfill(3)}'


    def generate_syndrome(self):
        self.comment('Syndrome')
        self.instruction('logic [EDC-1:0] w_syndrome;')
        for i in range(self.ecc_bits):
            syndrome_line = f'assign w_syndrome[{i}] = '
            start = False
            for j in range(self.total_bits):
                if (self.matrix[j] & (1 << i)):
                    if start:
                        syndrome_line += ' ^ '
                    if (j < self.ecc_bits):
                        syndrome_line += f'i_ecc[{self.ecc_bits-j-1}]'
                    else:
                        syndrome_line += f'i_data[{self.total_bits-j-1}]'
                    start = True
            syndrome_line += ';'
            self.instruction(syndrome_line)
        self.instruction('')


    def generate_data_repair(self):  # sourcery skip: extract-duplicate-method
        self.comment('Data Repair')
        self.instruction('always_comb begin')
        self.instruction('    o_data =  i_data;')
        self.instruction("    o_error =  1'b1;")
        self.instruction("    o_repairable =  1'b0;")
        self.instruction('    case (w_syndrome)')

        self.instruction(f"        {self.ecc_bits}'b{0:0{self.ecc_bits}b}: o_error = 1'b0;")
        for j in range(self.total_bits):
            self.instruction(f"        {self.ecc_bits}'b{self.matrix[j]:0{self.ecc_bits}b}: begin")
            if j >= self.total_bits - self.buswidth:
                bit = self.total_bits - j - 1
                self.instruction(f'            o_data[{bit}] = ~i_data[{bit}];')
                self.instruction("            o_repairable = 1'b1;")
            else:
                self.instruction("            o_repairable = 1'b0;")
            self.instruction('        end')
        self.instruction("        default: o_repairable = 1'b0;")
        self.instruction('    endcase // w_syndrome')
        self.instruction('end // always_comb')


    def verilog(self, file_path):  # sourcery skip: extract-duplicate-method
        self.comment('Generated by the Hamming Class; do not modify the code')
        self.generate_syndrome()
        self.generate_data_repair()
        self.instruction('')
        self.instruction('// synopsys translate_off')
        self.instruction('initial begin')
        self.instruction('    $dumpfile("dump.vcd");')
        self.instruction(f'    $dumpvars(0, {self.module_name});')
        self.instruction('end')
        self.instruction('// synopsys translate_on')
        self.instruction('')
        self.start()
        self.end()
        self.write(file_path, f'{self.module_name}.sv')

