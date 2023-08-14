`timescale 1ns / 1ps

module math_subtractor_full(input i_a, i_b, i_b_in, output ow_d, ow_b);

    assign ow_d = i_a ^ i_b ^ i_b_in;
    assign ow_b = (~i_a & i_b) | (~(i_a ^ i_b) & i_b_in);

endmodule : math_subtractor_full