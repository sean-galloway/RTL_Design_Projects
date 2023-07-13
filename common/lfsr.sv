`timescale 1ns / 1ps

module lfsr #(
    parameter N = 5       // LFSR width
)(
    input wire         clk, rst_n,
    input wire         enable,
    input wire         seed_load,
    input wire [N-1:0] seed_data,
    input wire [N-1:0] taps,        // Taps to XNor; see the attached pdf for the proper taps to use
    output reg [N-1:0] lfsr_data,
    output reg         lfsr_done
);

    reg [N-1:0] lfsr_reg;
    reg xnor_out;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            lfsr_reg <= 0;
        end
        else begin
            if (enable) begin
                if (seed_load) begin
                    lfsr_reg <= seed_data;
                end
                else begin
                    lfsr_reg <= {lfsr_reg[N-2:0], xnor_out};
                end
            end
        end
    end

    always_ff @(posedge clk) begin
        xnor_out <= ~^(lfsr_reg & taps);
    end

    assign lfsr_data = lfsr_reg;
    assign lfsr_done = (lfsr_reg[N:1] == seed_data) ? 1'b1 : 1'b0;

endmodule : lfsr
