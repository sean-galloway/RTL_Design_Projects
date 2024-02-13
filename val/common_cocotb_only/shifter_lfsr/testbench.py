import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.clock import Clock
import random

# Utility function to run an LFSR test with given parameters
async def run_lfsr_test(dut, seed_value, taps, N):
    clock = Clock(dut.i_clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut.i_rst_n.value = 0
    dut.i_seed_load.value = 0
    dut.i_seed_data.value = 0
    dut.i_tap0.value = 0
    dut.i_tap1.value = 0
    dut.i_tap2.value = 0
    dut.i_tap3.value = 0
    await Timer(10, units="ns")
    await FallingEdge(dut.i_clk)
    dut.i_rst_n.value = 1
    await FallingEdge(dut.i_clk)
    await FallingEdge(dut.i_clk)

    # Load the seed and configure the taps
    dut.i_seed_load.value = 1
    dut.i_seed_data.value = seed_value
    dut.i_tap0.value = taps[0]
    dut.i_tap1.value = taps[1]
    dut.i_tap2.value = taps[2]
    dut.i_tap3.value = taps[3]
    await FallingEdge(dut.i_clk)
    await FallingEdge(dut.i_clk)
    dut.i_seed_load.value = 0
    dut.i_enable.value = 1

    # Monitor the LFSR output
    cycle_count = 0
    while int(dut.o_lfsr_data.value) != seed_value:
        await FallingEdge(dut.i_clk)
        cycle_count += 1
        # Limit to prevent infinite loops, adjust as necessary
        if cycle_count > 2**N:  
            print("Failed to loop back to the initial seed within a reasonable number of cycles.")
            break

    dut.i_enable.value = 0  # Disable LFSR
    
    # Reporting
    print(f"For seed={seed_value:0{N}b} and taps={taps}, it took {cycle_count} cycles to repeat.")

# Master function to generate and schedule tests based on parameters
async def schedule_tests(dut):
    N = len(dut.i_seed_data)
    # Define your tests here, for example:
    seeds_and_taps = [
        (random.getrandbits(N), [8, 6, 5, 4]),  # Initial configuration
        # Add more configurations as needed
    ]

    for seed, taps in seeds_and_taps:
        await run_lfsr_test(dut, seed, taps, N)

# Entry point for the cocotb test
@cocotb.test()
async def dynamic_lfsr_tests(dut):
    await schedule_tests(dut)
