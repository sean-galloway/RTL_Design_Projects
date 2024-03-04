import cocotb
from cocotb.triggers import RisingEdge, Timer

from cocotb.clock import Clock
from cocotb.regression import TestFactory
import os
import subprocess
import random

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


TIMEOUT_CYCLES = 1000  # Adjust as necessary

@cocotb.coroutine
async def write_fifo(dut, data, delay_between_writes=0):
    dut.i_write.value = 0
    await RisingEdge(dut.i_wr_clk)
    await Timer(100, units='ps')  # Adding a 100 ps delay
    data_len = len(data)
    data_sent = 0
    timeout_counter = 0

    while data_sent != data_len:
        idx = data_sent
        # dut._log.info(f"Got Rising Edge of i_wr_clk (Iteration {idx}). Checking if FIFO full...")

        while dut.o_wr_full.value == 0 and (data_sent != data_len):
            value = data[data_sent]
            idx = data_sent
            dut.i_write.value = 1
            dut.i_wr_data.value = value
            data_sent += 1
            await RisingEdge(dut.i_wr_clk)
            await Timer(100, units='ps')  # Adding a 100 ps delay
            dut._log.info(f"Writing data {hex(value)} to FIFO (Iteration {idx})...")
            dut.i_write.value = 0

            for _ in range(delay_between_writes):
                await RisingEdge(dut.i_wr_clk)
                await Timer(100, units='ps')  # Adding a 100 ps delay

            timeout_counter += 1
            if timeout_counter >= TIMEOUT_CYCLES:
                dut._log.error("Timeout during write!")
                return

        # dut._log.info(f"FIFO is full. Waiting for next clock cycle (Iteration {idx})...")
        dut.i_write.value = 0
        dut.i_wr_data.value = 0
        await RisingEdge(dut.i_wr_clk)
        await Timer(100, units='ps')  # Adding a 100 ps delay

    dut.i_write.value = 0
    dut.i_wr_data.value = 0
    await RisingEdge(dut.i_wr_clk)
    await Timer(100, units='ps')  # Adding a 100 ps delay
    dut._log.info("Exiting write_fifo...")


@cocotb.coroutine
async def delayed_read_fifo(dut, delay, expected_data_length, delay_between_reads=0):
    dut._log.info(f"Entering delayed_read_fifo with delay {delay}...")
    read_values = []

    timeout_counter = 0
    while dut.o_wr_full.value != 1:
        await RisingEdge(dut.i_rd_clk)
        await Timer(100, units='ps')  # Adding a 100 ps delay
        timeout_counter += 1
        if timeout_counter >= TIMEOUT_CYCLES:
            dut._log.error("Timeout waiting for FIFO to fill!")
            return

    for _ in range(delay):
        await RisingEdge(dut.i_rd_clk)
        await Timer(100, units='ps')  # Adding a 100 ps delay

    data_read = 0
    timeout_counter = 0

    while data_read != expected_data_length:
        if dut.o_rd_empty.value == 1:
            dut.i_read.value = 0
            await RisingEdge(dut.i_rd_clk)
            await Timer(100, units='ps')  # Adding a 100 ps delay
            continue

        dut.i_read.value = 1
        read_data = int(dut.ow_rd_data.value)
        read_values.append(read_data)
        data_read += 1
        await RisingEdge(dut.i_rd_clk)
        await Timer(100, units='ps')  # Adding a 100 ps delay
        dut._log.info(f"Read data from FIFO: {hex(read_data)} (Iteration {data_read})")
        dut.i_read.value = 0

        for _ in range(delay_between_reads):
            await RisingEdge(dut.i_rd_clk)
            await Timer(100, units='ps')  # Adding a 100 ps delay

        timeout_counter += 1
        if timeout_counter >= TIMEOUT_CYCLES:
            dut._log.error("Timeout during read!")
            return

    dut.i_read.value = 0
    dut._log.info("Exiting delayed_read_fifo...")
    return read_values


@cocotb.test()
async def fifo_test(dut):
    # Use the seed for reproducibility
    # Now that we know where the sim_build directory is, configure logging
    log_path = os.environ.get('LOG_PATH')
    dut_name = os.environ.get('DUT')
    log = configure_logging(dut_name, log_path)
    seed = int(os.environ.get('SEED', '0'))
    random.seed(seed)
    log.info(f'seed changed to {seed}')

    dut.i_write.value = 0
    dut.i_read.value = 0
    dut.i_wr_data.value = 0
    dut.i_wr_rst_n.value = 0
    dut.i_rd_rst_n.value = 0

    cocotb.start_soon(Clock(dut.i_wr_clk, 10, units="ns").start())
    cocotb.start_soon(Clock(dut.i_rd_clk, 15, units="ns").start())

    await Timer(300, units="ns")
    dut.i_wr_rst_n.value = 1
    dut.i_rd_rst_n.value = 1

    width = 8
    depth = 10
    iterations = 100
    delay_between_iterations = 20

    for _ in range(iterations):
        data = [random.randint(0, (1 << width) - 1) for _ in range(2*depth)]
        write_delay = random.randint(0, 10)
        cocotb.fork(write_fifo(dut, data, write_delay))
        read_delay = random.randint(0, 10)
        read2read_delay = random.randint(0, 2)
        read_values = await delayed_read_fifo(dut, read_delay, len(data), read2read_delay)

        hex_data = [hex(num) for num in data]
        hex_read_data = [hex(num) for num in read_values]
        assert data == read_values, f"Data mismatch. Written: {hex_data}, Read: {hex_read_data}"


        for _ in range(delay_between_iterations):
            await RisingEdge(dut.i_rd_clk)
            await Timer(100, units='ps')  # Adding a 100 ps delay

tf = TestFactory(fifo_test)
tf.generate_tests()

repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
tests_dir = os.path.abspath(os.path.dirname(__file__)) #gives the path to the test(current) directory in which this test.py file is placed
rtl_dir = os.path.abspath(os.path.join(repo_root, 'rtl/', 'common')) #path to hdl folder where .v files are placed

@pytest.mark.parametrize("depth, data_width, almost_wr_margin, almost_rd_margin", [(10, 8, 2, 2)])
def test_fifo_async_div2(request, depth, data_width, almost_wr_margin, almost_rd_margin):
    dut_name = "fifo_async_div2"
    module = os.path.splitext(os.path.basename(__file__))[0]  # The name of this file
    toplevel = "fifo_async_div2"   

    verilog_sources = [
        os.path.join(rtl_dir, "find_first_set.sv"),
        os.path.join(rtl_dir, "find_last_set.sv"),
        os.path.join(rtl_dir, "leading_one_trailing_one.sv"),
        os.path.join(rtl_dir, "counter_bin.sv"),
        os.path.join(rtl_dir, "counter_johnson.sv"),
        os.path.join(rtl_dir, "grayj2bin.sv"),
        os.path.join(rtl_dir, "glitch_free_n_dff_arn.sv"),
        os.path.join(rtl_dir, "fifo_control.sv"),
        os.path.join(rtl_dir, "fifo_async_div2.sv"),

    ]
    parameters = {'DEPTH':depth,'DATA_WIDTH':data_width,'ALMOST_WR_MARGIN':almost_wr_margin,'ALMOST_RD_MARGIN':almost_rd_margin, }

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
