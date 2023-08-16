`timescale 1ns / 1ps

module math_addsub_full_nbit #(parameter N=4) (
    input  logic [N-1:0]   i_a,
    input  logic [N-1:0]   i_b,
    input  logic           i_c,           // 0 for add, 1 for subtract
    output logic [N-1:0]   ow_sum,
    output logic           ow_c           // Final carry-out
    );

    logic [N:0]   w_c;   // array for internal carries
    logic [N-1:0] w_ip;  // array XORing i_c and i_b

    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : GEN_XOR
            assign w_ip[i] = i_b[i] ^ i_c;
        end
    endgenerate

    assign w_c[0] = i_c;

    generate
        for (i = 0; i < N; i = i + 1) begin : GEN_FULL_ADDERS
            math_adder_full fa(
                .i_a     (i_a[i]),
                .i_b     (w_ip[i]),
                .i_c     (w_c[i]),
                .ow_sum  (ow_sum[i]),
                .ow_c    (w_c[i+1])
            );
        end
    endgenerate

    assign ow_c = w_c[N]; // output the final carry or borrow

    // synopsys translate_off
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, math_addsub_full_nbit);
    end
    // synopsys translate_on

endmodule : math_addsub_full_nbit
