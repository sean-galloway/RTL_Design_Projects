import sys
import argparse


def generate_partial_products(N, f):
    # Generate partial products
    f.write("// Partial products generation\n")

    # Define bit groups here, then populate it as we generate the partial products
    bit_groups = {i: [] for i in range(2 * N)}

    # Determine the max number of digits needed
    max_digits = len(str(N - 1))
    
    for i in range(N):
        for j in range(N):
            formatted_i = str(i).zfill(max_digits)
            formatted_j = str(j).zfill(max_digits)

            f.write(f"wire w_pp_{formatted_i}_{formatted_j} = i_multiplier[{i:2}] & i_multiplicand[{j:2}];\n")
            bit_groups[i + j].append(f"w_pp_{formatted_i}_{formatted_j}")

    f.write("\n")
    return bit_groups


def dadda_reduction(bit_groups, N, f):
    def next_smaller_dadda_number(n):
        # This function returns the next smaller number of partial products after reducing with Dadda's method.
        # For example, if you start with 13 partial products, the next goal is 9, then 6, then 4, then 3, and finally 2.
        if n > 6:
            return 6
        elif n > 4:
            return 4
        elif n > 3:
            return 3
        else:
            return 2

    f.write("// Partial products reduction using Dadda tree\n")
    max_digits_idx = len(str(2 * N - 1))
    max_digits_len = len(str(max(len(group) for group in bit_groups.values())))

    for bit_idx in range(2 * N - 1):
        goal = next_smaller_dadda_number(len(bit_groups[bit_idx]))
        while len(bit_groups[bit_idx]) > goal:
            while len(bit_groups[bit_idx]) > 2:
                a, b, c = bit_groups[bit_idx][:3]
                formatted_idx = str(bit_idx).zfill(max_digits_idx)
                formatted_len = str(len(bit_groups[bit_idx])).zfill(max_digits_len)

                sum_name = f"w_sum_{formatted_idx}_{formatted_len}"
                carry_name = f"w_carry_{formatted_idx}_{formatted_len}"

                f.write(f"wire {sum_name}, {carry_name};\n")
                f.write(f"math_adder_carry_save CSA_{formatted_idx}_{formatted_len}(.i_a({a}), .i_b({b}), .i_c({c}), .ow_sum({sum_name}), .ow_c({carry_name}));\n")

                bit_groups[bit_idx] = bit_groups[bit_idx][3:]
                bit_groups[bit_idx].append(sum_name)
                bit_groups[bit_idx + 1].append(carry_name)

            while len(bit_groups[bit_idx]) == 2:
                a, b = bit_groups[bit_idx][:2]
                formatted_idx = str(bit_idx).zfill(max_digits_idx)
                formatted_len = str(len(bit_groups[bit_idx])).zfill(max_digits_len)

                sum_name = f"w_sum_{formatted_idx}_{formatted_len}"
                carry_name = f"w_carry_{formatted_idx}_{formatted_len}"

                f.write(f"wire {sum_name}, {carry_name};\n")
                f.write(f"math_adder_half HA_{formatted_idx}_{formatted_len}(.i_a({a}), .i_b({b}), .ow_sum({sum_name}), .ow_c({carry_name}));\n")

                bit_groups[bit_idx] = bit_groups[bit_idx][2:]
                bit_groups[bit_idx].append(sum_name)
                bit_groups[bit_idx + 1].append(carry_name)

    f.write("\n")


def wallace_reduction(bit_groups, N, f, multiplier_type):
    f.write("// Partial products reduction using Wallace tree\n")

    max_digits_idx = len(str(2 * N - 1))
    max_digits_len = len(str(max(len(group) for group in bit_groups.values())))

    for bit_idx in range(2 * N - 1):
        while len(bit_groups[bit_idx]) > 2:
            a, b, c = bit_groups[bit_idx][:3]
            formatted_idx = str(bit_idx).zfill(max_digits_idx)
            formatted_len = str(len(bit_groups[bit_idx])).zfill(max_digits_len)

            sum_name = f"w_sum_{formatted_idx}_{formatted_len}"
            carry_name = f"w_carry_{formatted_idx}_{formatted_len}"

            f.write(f"wire {sum_name}, {carry_name};\n")

            if multiplier_type == "wfa":
                f.write(f"math_adder_full FA_{formatted_idx}_{formatted_len}(.i_a({a}), .i_b({b}), .i_c({c}), .ow_sum({sum_name}), .ow_c({carry_name}));\n")
            else:
                f.write(f"math_adder_carry_save CSA_{formatted_idx}_{formatted_len}(.i_a({a}), .i_b({b}), .i_c({c}), .ow_sum({sum_name}), .ow_c({carry_name}));\n")

            bit_groups[bit_idx] = bit_groups[bit_idx][3:]
            bit_groups[bit_idx].append(sum_name)
            bit_groups[bit_idx + 1].append(carry_name)

        while len(bit_groups[bit_idx]) == 2:
            a, b = bit_groups[bit_idx][:2]
            formatted_idx = str(bit_idx).zfill(max_digits_idx)
            formatted_len = str(len(bit_groups[bit_idx])).zfill(max_digits_len)

            sum_name = f"w_sum_{formatted_idx}_{formatted_len}"
            carry_name = f"w_carry_{formatted_idx}_{formatted_len}"

            f.write(f"wire {sum_name}, {carry_name};\n")
            f.write(f"math_adder_half HA_{formatted_idx}_{formatted_len}(.i_a({a}), .i_b({b}), .ow_sum({sum_name}), .ow_c({carry_name}));\n")

            bit_groups[bit_idx] = bit_groups[bit_idx][2:]
            bit_groups[bit_idx].append(sum_name)
            bit_groups[bit_idx + 1].append(carry_name)

    f.write("\n")


def generate_final_addition(bit_groups, N, f):
    # This function will generate the final addition stage.
    max_digits_bit = len(str(2*N - 1))
    products = {bit_idx: len(bit_groups[bit_idx]) for bit_idx in bit_groups}

    # Prepare output for bit by bit addition
    f.write("// Final addition stage\n")
    previous_carry = None
    for bit in range(2*N):
        formatted_bit = str(bit).zfill(max_digits_bit)

        sum_name = f"ow_sum_{formatted_bit}"
        carry_name = f"ow_carry_{formatted_bit}"
        variables = bit_groups.get(bit, [])

        # if no variables are present for this bit, just output a 0
        if not variables:
            f.write(f"assign {sum_name} = 1'b0;\n")
            continue

        if len(variables) == 1:
            f.write(f"assign {sum_name} = {variables[0]};\n")
        else:
            # Wire the sum and carry
            f.write(f"wire {sum_name}, {carry_name};\n")
            
            ic_value = previous_carry or "1'b0"
            fa_line = f"math_adder_full FA_{formatted_bit}(.i_a({variables[0]}), .i_b({variables[1]}), .i_c({ic_value}), .ow_sum({sum_name}), .ow_c({carry_name}));\n"
            f.write(fa_line)

        previous_carry = carry_name

    f.write("\n")


def generate_final_assignments(N, f):
    f.write("// Final product assignment\n")

    # Calculate the maximum number of digits required
    max_digits = len(str(2 * N - 1))

    for i in range(2 * N):
        formatted_idx = str(i).zfill(max_digits)
        f.write(f"assign ow_product[{i}] = ow_sum_{formatted_idx};\n")

    f.write("\n")


def generate_tree(N, multiplier_type):
    if multiplier_type == 'wcsa':
        name = f"math_multiplier_wallace_tree_csa_{N}"
        title = 'Wallace Tree CSA'
    elif multiplier_type == 'wfa':
        name = f"math_multiplier_wallace_tree_{N}"
        title = 'Wallace Tree FA'
    else:
        name = f"math_multiplier_dadda_tree_{N}"
        title = 'Dadda Tree CSA'

    filename =f'{name}.sv'
    with open(filename, 'w') as f:
        _generate_tree_helper(f, multiplier_type, N, name)
    print(f"{title} multiplier for N={N} using {multiplier_type} generated and saved as '{filename}'.")


def _generate_tree_helper(f, multiplier_type, N, name):
    f.write(f"`timescale 1ns / 1ps\n\n")
    f.write(f"module {name} (\n")
    f.write(f"    input  [{N - 1}:0] i_multiplier,\n")
    f.write(f"    input  [{N - 1}:0] i_multiplicand,\n")
    f.write(f"    output [{2 * N - 1}:0] ow_product\n")
    f.write(f");\n\n")

    bit_groups = generate_partial_products(N, f)
    if multiplier_type == "dad":
        dadda_reduction(bit_groups, N, f)
    else:
        wallace_reduction(bit_groups, N, f, multiplier_type)

    generate_final_addition(bit_groups, N, f)
    generate_final_assignments(N, f)

    f.write(f'''
    // Debug purposes
    // synopsys translate_off
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, {name});
    end
    // synopsys translate_off
        ''')

    f.write(f"\nendmodule : {name}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Wallace/Dadda Tree Multiplier for given N")
    parser.add_argument("-n", required=True, type=int, help="Specify the size N for the Wallace Tree Multiplier")
    parser.add_argument("-t", required=True, choices=["wfa", "wcsa", "dad"], help="Specify the type: wfa for Wallace Full Adder, wcsa for Wallace Carry Save Adder, or dad for Dadda Multiplier")

    args = parser.parse_args()

    if not args.n:
        print("Usage: python generate_wallace_tree.py -n <N> -t <type>")
        sys.exit(1)

    N = args.n
    multiplier_type = args.t
    generate_tree(N, multiplier_type)
