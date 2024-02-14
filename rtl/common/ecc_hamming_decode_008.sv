`timescale 1ns / 1ps

module ecc_hamming_decode_008 #(parameter int  N = 8,
parameter int  ECC = 4)(
    input  logic [N-1:0]   i_data,
    input  logic [ECC-1:0] i_ecc,
    output logic [N-1:0]   o_data,
    output logic           o_error,
    output logic           o_repairable
);

// Generated by the Hamming Class; do not modify the code
// Syndrome
logic [EDC-1:0] w_syndrome;
assign w_syndrome[0] = i_ecc[3] ^ i_data[7] ^ i_data[6] ^ i_data[4] ^ i_data[3] ^ i_data[1];
assign w_syndrome[1] = i_ecc[2] ^ i_data[7] ^ i_data[5] ^ i_data[4] ^ i_data[2] ^ i_data[1];
assign w_syndrome[2] = i_ecc[1] ^ i_data[6] ^ i_data[5] ^ i_data[4] ^ i_data[0];
assign w_syndrome[3] = i_ecc[0] ^ i_data[3] ^ i_data[2] ^ i_data[1] ^ i_data[0];

// Data Repair
always_comb begin
    o_data =  i_data;
    o_error =  1'b1;
    o_repairable =  1'b0;
    case (w_syndrome)
        4'b0000: o_error = 1'b0;
        4'b0001: begin
            o_repairable = 1'b0;
        end
        4'b0010: begin
            o_repairable = 1'b0;
        end
        4'b0100: begin
            o_repairable = 1'b0;
        end
        4'b1000: begin
            o_repairable = 1'b0;
        end
        4'b0011: begin
            o_data[7] = ~i_data[7];
            o_repairable = 1'b1;
        end
        4'b0101: begin
            o_data[6] = ~i_data[6];
            o_repairable = 1'b1;
        end
        4'b0110: begin
            o_data[5] = ~i_data[5];
            o_repairable = 1'b1;
        end
        4'b0111: begin
            o_data[4] = ~i_data[4];
            o_repairable = 1'b1;
        end
        4'b1001: begin
            o_data[3] = ~i_data[3];
            o_repairable = 1'b1;
        end
        4'b1010: begin
            o_data[2] = ~i_data[2];
            o_repairable = 1'b1;
        end
        4'b1011: begin
            o_data[1] = ~i_data[1];
            o_repairable = 1'b1;
        end
        4'b1100: begin
            o_data[0] = ~i_data[0];
            o_repairable = 1'b1;
        end
        default: o_repairable = 1'b0;
    endcase // w_syndrome
end // always_comb

// synopsys translate_off
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, ecc_hamming_decode_008);
end
// synopsys translate_on

endmodule
