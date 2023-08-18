import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure

@cocotb.test()
async def test_full_adder(dut):
    """ Test the full adder for all possible input combinations """
    
    # Define the expected results for all input combinations in the format:
    # (i_a, i_b, i_c) -> (ow_sum, ow_c)
    expected_results = {
        (0, 0, 0): (0, 0),
        (0, 0, 1): (1, 0),
        (0, 1, 0): (1, 0),
        (0, 1, 1): (0, 1),
        (1, 0, 0): (1, 0),
        (1, 0, 1): (0, 1),
        (1, 1, 0): (0, 1),
        (1, 1, 1): (1, 1)
    }

    for inputs, expected_output in expected_results.items():
        dut.i_a.value = inputs[0]
        dut.i_b.value = inputs[1]
        dut.i_c.value = inputs[2]

        await Timer(1, units='ns')  # wait for the combinatorial logic to settle

        if (dut.ow_sum.value, dut.ow_c.value) != expected_output:
            raise TestFailure(f"For inputs {inputs}, expected output was {expected_output} but got {(dut.ow_sum.value, dut.ow_c.value)}")