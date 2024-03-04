import cocotb
import itertools
from cocotb.triggers import Timer
from cocotb.regression import TestFactory
import os
import subprocess
import pytest
from cocotb_test.simulator import run
import logging

def configure_logging(dut_name, log_file_path):
    log = logging.getLogger(f'cocotb_log_{dut_name}')
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


@cocotb.test()
async def cla_4bit_test(dut):
    """ Test the 4-bit carry lookahead adder for all possible input combinations """
    # Now that we know where the sim_build directory is, configure logging
    log_path = os.environ.get('LOG_PATH')
    dut_name = os.environ.get('DUT')
    log = configure_logging(dut_name, log_path)
    N = 4
    for i_a, i_b in itertools.product(range(2**N), range(2**N)):
        for i_c in [0, 1]:
            # Apply inputs
            dut.i_a.value = i_a
            dut.i_b.value = i_b
            dut.i_c.value = i_c

            await Timer(1, units='ns')  # wait for the combinatorial logic to settle

            # Expected sum and carry out
            expected_sum = i_a + i_b + i_c
            expected_carry = 1 if expected_sum >= (2**N) else 0

            # Mask to get only N-bits for the sum
            expected_sum &= (2**N) - 1

            assert (int(dut.ow_sum) == expected_sum) and (int(dut.ow_carry) == expected_carry),\
                f"For i_a={i_a}, i_b={i_b}, and i_c={i_c}, expected sum was {expected_sum} and carry out was {expected_carry} but got sum={(dut.ow_sum.value)} and carry out={dut.ow_carry.value}"

tf = TestFactory(cla_4bit_test)
tf.generate_tests()

repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
tests_dir = os.path.abspath(os.path.dirname(__file__)) #gives the path to the test(current) directory in which this test.py file is placed
rtl_dir = os.path.abspath(os.path.join(repo_root, 'rtl/', 'common')) #path to hdl folder where .v files are placed

@pytest.mark.parametrize("n", [4])
def test_math_adder_carry_lookahead(request, n):
    dut_name = "math_adder_carry_lookahead"
    module = os.path.splitext(os.path.basename(__file__))[0]  # The name of this file
    toplevel = "math_adder_carry_lookahead"   

    verilog_sources = [
        os.path.join(rtl_dir, "math_adder_carry_lookahead.sv"),

    ]
    parameters = {'N':n, }

    extra_env = {f'PARAM_{k}': str(v) for k, v in parameters.items()}

    # sourcery skip: no-conditionals-in-tests
    if request.config.getoption("--regression"):
        sim_build = os.path.join(repo_root, 'val', 'unit', 'regression_area', 'sim_build', request.node.name.replace('[', '-').replace(']', ''))
    else:
        sim_build = os.path.join(repo_root, 'val', 'unit', 'local_sim_build', request.node.name.replace('[', '-').replace(']', ''))

    extra_env['LOG_PATH'] = os.path.join(str(sim_build), f'cocotb_log_{dut_name}.log')
    extra_env['DUT'] = dut_name

    run(
        python_search=[tests_dir],  # where to search for all the python test files
        verilog_sources=verilog_sources,
        toplevel=toplevel,
        module=module,
        parameters=parameters,
        sim_build=sim_build,
        extra_env=extra_env,
        waves=True,
    )