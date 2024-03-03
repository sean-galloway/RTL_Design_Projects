import cocotb
from cocotb.triggers import Timer
from cocotb.regression import TestFactory

import pytest
from cocotb_test.simulator import run
import logging
log = logging.getLogger('cocotb_log_count_leading_zeros')
log.setLevel(logging.DEBUG)
# Create a file handler that logs even debug messages
fh = logging.FileHandler('cocotb_log_count_leading_zeros.log')
fh.setLevel(logging.DEBUG)
# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# Add the handler to the logger
log.addHandler(fh)


@cocotb.test()
async def test_count_leading_zeros(dut):
    width = len(dut.i_data)
    dut._log.info(f"Testing with WIDTH={width}")

    # Start with all zeros
    dut.i_data.value = 0
    # dut.i_enable.value = 0
    await Timer(100, units='ns')
    # dut.i_enable.value = 1
    await Timer(10, units='ns')
    assert dut.ow_count_leading_zeros.value == width, f"Expected {width} leading zeros, got {dut.ow_leading_zeros_count.value}"

    # Walk a '1' through the entire width
    for i in range(width):
        dut.i_data.value = 1 << (width - 1 - i)
        await Timer(10, units='ns')
        expected_leading_zeros = width - 1 - i
        assert dut.ow_count_leading_zeros.value == expected_leading_zeros, f"Expected {expected_leading_zeros} leading zeros, got {dut.ow_leading_zeros_count.value}"

    # End with all zeros again
    dut.i_data.value = 0
    await Timer(10, units='ns')
    assert dut.ow_count_leading_zeros.value == width, f"Expected {width} leading zeros, got {dut.ow_leading_zeros_count.value}"

    dut._log.info("Test completed successfully")

tf = TestFactory(test_count_leading_zeros)
tf.generate_tests()