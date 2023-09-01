`timescale 1ns / 1ps

module math_adder_kogge_stone_nbit #(parameter N=4) (
    input  logic [N-1:0] i_a,
    input  logic [N-1:0] i_b,
    output logic [N-1:0] ow_sum,
    output logic         ow_carry
);

    // Step 1: Generate and Propagate terms
    logic [N-1:0] w_G, w_P;
    genvar i;
    for (i = 0; i < N; i=i+1) begin
        assign w_G[i] = i_a[i] & i_b[i];
        assign w_P[i] = i_a[i] | i_b[i];
    end

    // Step 2: Parallel Prefix Computation using Kogge-Stone
    logic [N-1:0] w_C;  // Array to store carry for each bit
    assign w_C[0] = w_G[0]; // Initial carry is the first generate signal
    generate
        for (i = 1; i < N; i=i+1) begin : GEN_KOGGE_STONE
            assign w_C[i] = w_G[i] | (w_P[i] & w_C[i-1]);
        end
    endgenerate

    // Step 3: Sum Calculation
    generate
        for (i = 0; i < N; i = i + 1) begin : GEN_SUM
            if (i == 0) begin
                assign ow_sum[i] = i_a[i] ^ i_b[i];
            end else begin
                assign ow_sum[i] = i_a[i] ^ i_b[i] ^ w_C[i-1];
            end
        end
    endgenerate
    

    // The final carry out
    assign ow_carry = w_C[N-1];

    // Debug purposes
    // synopsys translate_off
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, math_adder_kogge_stone_nbit);
    end
    // synopsys translate_off


endmodule : math_adder_kogge_stone_nbit
