import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, Timer
from cocotb.clock import Clock
import random
import os
import subprocess
import pytest
from cocotb_test.simulator import run
import logging
import random
from cam_testing import CamTB


@cocotb.test()
async def basic_test(dut):
    '''Test the CAM as thoroughly as possible'''
    tb = CamTB(dut)
    # Use the seed for reproducibility
    seed = int(os.environ.get('SEED', '0'))
    random.seed(seed)
    tb.log.info(f'seed changed to {seed}')
    # TB Setup and reset sequence
    tb.print_settings()
    await tb.start_clock('i_clk', 10, 'ns')
    await tb.assert_reset()
    await tb.wait_clocks('i_clk', 5)
    await tb.deassert_reset()
    await tb.wait_clocks('i_clk', 5)
    tb.log.info("Starting test...")

    tb.check_empty()   # should start off empty
    tb.check_not_full() # should not be full either

    # Test Cases for one entry
    await tb.mark_one_valid(0x5A)
    tb.check_not_empty()
    tb.check_not_full()
    await tb.check_tag(0x5A, 1) # make sure it is true
    await tb.check_tag(0xA5, 0) # make sure it is false
    await tb.mark_one_invalid(0xA5)  # should be illegal
    await tb.check_tag(0x5A, 1) # make sure it is true
    await tb.check_tag(0xA5, 0) # make sure it is false
    await tb.mark_one_invalid(0x5A)  # clear it out
    tb.check_empty()   # should start off empty
    tb.check_not_full() # should not be full either
    await tb.mark_one_invalid(0x5A)  # clear it out
    tb.check_empty()   # should start off empty
    tb.check_not_full() # should not be full either
    await tb.main_loop()

    tb.log.info("Test completed successfully.")

repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
tests_dir = os.path.abspath(os.path.dirname(__file__)) #gives the path to the test(current) directory in which this test.py file is placed
rtl_dir = os.path.abspath(os.path.join(repo_root, 'rtl/', 'common')) #path to hdl folder where .v files are placed

@pytest.mark.parametrize("n, depth", [(8, 16)])
def test_cam_tag(request, n, depth):
    dut_name = "cam_tag"
    module = os.path.splitext(os.path.basename(__file__))[0]  # The name of this file
    toplevel = "cam_tag"   

    verilog_sources = [
        os.path.join(rtl_dir, "find_first_set.sv"),
        os.path.join(rtl_dir, "find_last_set.sv"),
        os.path.join(rtl_dir, "leading_one_trailing_one.sv"),
        os.path.join(rtl_dir, "cam_tag.sv"),
    ]
    parameters = {'N':n,'DEPTH':depth}

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