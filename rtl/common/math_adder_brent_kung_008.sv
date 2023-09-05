module math_adder_brent_kung_008 #(parameter N=8)(
    input  logic [N-1:0] i_a,
    input  logic [N-1:0] i_b,
    input  logic         i_c,
    output logic [N-1:0] ow_sum,
    output logic         ow_carry
);

logic [N:0] ow_g;
logic [N:0] ow_p;
logic [N:0] ow_gg;
math_adder_brent_kung_bitwisepg #(.N(N)) BitwisePGLogic_inst(.i_a(i_a),.i_b(i_b),.i_c(i_c),.ow_g(ow_g),.ow_p(ow_p));
math_adder_brent_kung_grouppg_008 #(.N(N)) GroupPGLogic_inst(.i_g(ow_g),.i_p(ow_p),.ow_gg(ow_gg));
math_adder_brent_kung_sum #(.N(N)) SumLogic_inst(.i_p(ow_p),.i_gg(ow_gg),.ow_sum(ow_sum),.ow_carry(ow_carry));
// synopsys translate_off
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, math_adder_brent_kung_008);
end
// synopsys translate_on

endmodule