import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
from cocotb.regression import TestFactory
import itertools
import os
import subprocess
import pytest
from cocotb_test.simulator import run
import logging
log = logging.getLogger('cocotb_log_math_subtractor_ripple_carry')
log.setLevel(logging.DEBUG)
# Create a file handler that logs even debug messages
fh = logging.FileHandler('cocotb_log_math_subtractor_ripple_carry.log')
fh.setLevel(logging.DEBUG)
# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# Add the handler to the logger
log.addHandler(fh)


@cocotb.test()
async def subtractor_test(dut):
    """ Test for 4-bit ripple carry subtractor """
    N = 4
    width_mask = (1 << N) - 1

    for i_a, i_b in itertools.product(range(2**N), repeat=2):
        for i_borrow_in in range(2):
            dut.i_a.value = i_a
            dut.i_b.value = i_b
            dut.i_borrow_in.value = i_borrow_in

            await Timer(1, units='ns')

            expected_difference = (i_a - i_b - i_borrow_in) & width_mask
            expected_carry_out = 1 if (i_a - i_b - i_borrow_in) < 0 else 0

            if int(dut.ow_difference.value) != expected_difference or int(dut.ow_carry_out.value) != expected_carry_out:
                raise TestFailure(f"For i_a={i_a}, i_b={i_b}, i_borrow_in={i_borrow_in}, expected difference was {expected_difference} and carry out was {expected_carry_out} but got difference={dut.ow_difference.value} and carry out={dut.ow_carry_out.value}")


tf = TestFactory(subtractor_test)
tf.generate_tests()

repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
tests_dir = os.path.abspath(os.path.dirname(__file__)) #gives the path to the test(current) directory in which this test.py file is placed
rtl_dir = os.path.abspath(os.path.join(repo_root, 'rtl/', 'common')) #path to hdl folder where .v files are placed

@pytest.mark.parametrize("n", [(4,)])
def test_math_subtractor_ripple_carry(request, n):
    dut = "math_subtractor_carry_lookahead"
    module = os.path.splitext(os.path.basename(__file__))[0]  # The name of this file
    toplevel = "math_subtractor_carry_lookahead"   

    verilog_sources = [
        os.path.join(rtl_dir, "math_subtractor_carry_lookahead.sv"),

    ]
    parameters = {'N':n, }

    extra_env = {f'PARAM_{k}': str(v) for k, v in parameters.items()}

    # sourcery skip: no-conditionals-in-tests
    if request.config.getoption("--regression"):
        sim_build = os.path.join('regression_area', 'sim_build', request.node.name.replace('[', '-').replace(']', ''))
    else:
        sim_build = os.path.join('local_sim_build', request.node.name.replace('[', '-').replace(']', ''))

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
