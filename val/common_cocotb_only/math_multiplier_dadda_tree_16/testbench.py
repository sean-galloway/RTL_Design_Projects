import cocotb
import itertools
from cocotb.regression import TestFactory
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
from cocotb.triggers import Timer
import random

@cocotb.coroutine
def init_test(dut):
    dut.i_multiplier.value = 0
    dut.i_multiplicand.value = 0
    yield Timer(1, units='ns')

@cocotb.test()
def multiplier_dadda_tree_16_test(dut): 

    yield init_test(dut)

    N = 16
    max_val = 2**N
    for _ in range(10000):
    # for a, b in itertools.product(range(max_val), range(max_val)):
        a = random.randint(0, max_val-1)
        b = random.randint(0, max_val-1)
        dut.i_multiplier.value = a
        dut.i_multiplicand.value = b

        yield Timer(10, units='ns')
        # print(f"Multiplier: {dut.i_multiplier.value}, Multiplicand: {dut.i_multiplicand.value}")

        result = dut.ow_product.value.integer
        expected_result = a * b
        assert result == expected_result, f"Multiplication of {a} and {b} yielded {result}, expected {expected_result}"

tf = TestFactory(multiplier_dadda_tree_16_test)
tf.generate_tests()
