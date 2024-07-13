
`timescale 1ns / 1ps

module apb_xbar_thin_wrap_m10_s10 #(
    parameter int M = 10,
    parameter int S = 10,
    parameter int ADDR_WIDTH = 32,
    parameter int DATA_WIDTH = 32,
    parameter int STRB_WIDTH = 32/8,
    parameter int DW  = DATA_WIDTH,
    parameter int AW  = ADDR_WIDTH,
    parameter int SW  = STRB_WIDTH
) (
    input  logic                 aclk,
    input  logic                 aresetn,

    input  logic                 m0_apb_psel,
    input  logic                 m0_apb_penable,
    input  logic                 m0_apb_pwrite,
    input  logic [2:0]           m0_apb_pprot,
    input  logic [AW-1:0]        m0_apb_paddr,
    input  logic [DW-1:0]        m0_apb_pwdata,
    input  logic [SW-1:0]        m0_apb_pstrb,
    output logic                 m0_apb_pready,
    output logic [DW-1:0]        m0_apb_prdata,
    output logic                 m0_apb_pslverr,

    input  logic                 m1_apb_psel,
    input  logic                 m1_apb_penable,
    input  logic                 m1_apb_pwrite,
    input  logic [2:0]           m1_apb_pprot,
    input  logic [AW-1:0]        m1_apb_paddr,
    input  logic [DW-1:0]        m1_apb_pwdata,
    input  logic [SW-1:0]        m1_apb_pstrb,
    output logic                 m1_apb_pready,
    output logic [DW-1:0]        m1_apb_prdata,
    output logic                 m1_apb_pslverr,

    input  logic                 m2_apb_psel,
    input  logic                 m2_apb_penable,
    input  logic                 m2_apb_pwrite,
    input  logic [2:0]           m2_apb_pprot,
    input  logic [AW-1:0]        m2_apb_paddr,
    input  logic [DW-1:0]        m2_apb_pwdata,
    input  logic [SW-1:0]        m2_apb_pstrb,
    output logic                 m2_apb_pready,
    output logic [DW-1:0]        m2_apb_prdata,
    output logic                 m2_apb_pslverr,

    input  logic                 m3_apb_psel,
    input  logic                 m3_apb_penable,
    input  logic                 m3_apb_pwrite,
    input  logic [2:0]           m3_apb_pprot,
    input  logic [AW-1:0]        m3_apb_paddr,
    input  logic [DW-1:0]        m3_apb_pwdata,
    input  logic [SW-1:0]        m3_apb_pstrb,
    output logic                 m3_apb_pready,
    output logic [DW-1:0]        m3_apb_prdata,
    output logic                 m3_apb_pslverr,

    input  logic                 m4_apb_psel,
    input  logic                 m4_apb_penable,
    input  logic                 m4_apb_pwrite,
    input  logic [2:0]           m4_apb_pprot,
    input  logic [AW-1:0]        m4_apb_paddr,
    input  logic [DW-1:0]        m4_apb_pwdata,
    input  logic [SW-1:0]        m4_apb_pstrb,
    output logic                 m4_apb_pready,
    output logic [DW-1:0]        m4_apb_prdata,
    output logic                 m4_apb_pslverr,

    input  logic                 m5_apb_psel,
    input  logic                 m5_apb_penable,
    input  logic                 m5_apb_pwrite,
    input  logic [2:0]           m5_apb_pprot,
    input  logic [AW-1:0]        m5_apb_paddr,
    input  logic [DW-1:0]        m5_apb_pwdata,
    input  logic [SW-1:0]        m5_apb_pstrb,
    output logic                 m5_apb_pready,
    output logic [DW-1:0]        m5_apb_prdata,
    output logic                 m5_apb_pslverr,

    input  logic                 m6_apb_psel,
    input  logic                 m6_apb_penable,
    input  logic                 m6_apb_pwrite,
    input  logic [2:0]           m6_apb_pprot,
    input  logic [AW-1:0]        m6_apb_paddr,
    input  logic [DW-1:0]        m6_apb_pwdata,
    input  logic [SW-1:0]        m6_apb_pstrb,
    output logic                 m6_apb_pready,
    output logic [DW-1:0]        m6_apb_prdata,
    output logic                 m6_apb_pslverr,

    input  logic                 m7_apb_psel,
    input  logic                 m7_apb_penable,
    input  logic                 m7_apb_pwrite,
    input  logic [2:0]           m7_apb_pprot,
    input  logic [AW-1:0]        m7_apb_paddr,
    input  logic [DW-1:0]        m7_apb_pwdata,
    input  logic [SW-1:0]        m7_apb_pstrb,
    output logic                 m7_apb_pready,
    output logic [DW-1:0]        m7_apb_prdata,
    output logic                 m7_apb_pslverr,

    input  logic                 m8_apb_psel,
    input  logic                 m8_apb_penable,
    input  logic                 m8_apb_pwrite,
    input  logic [2:0]           m8_apb_pprot,
    input  logic [AW-1:0]        m8_apb_paddr,
    input  logic [DW-1:0]        m8_apb_pwdata,
    input  logic [SW-1:0]        m8_apb_pstrb,
    output logic                 m8_apb_pready,
    output logic [DW-1:0]        m8_apb_prdata,
    output logic                 m8_apb_pslverr,

    input  logic                 m9_apb_psel,
    input  logic                 m9_apb_penable,
    input  logic                 m9_apb_pwrite,
    input  logic [2:0]           m9_apb_pprot,
    input  logic [AW-1:0]        m9_apb_paddr,
    input  logic [DW-1:0]        m9_apb_pwdata,
    input  logic [SW-1:0]        m9_apb_pstrb,
    output logic                 m9_apb_pready,
    output logic [DW-1:0]        m9_apb_prdata,
    output logic                 m9_apb_pslverr,

    output logic                 s0_apb_psel,
    output logic                 s0_apb_penable,
    output logic                 s0_apb_pwrite,
    output logic [2:0]           s0_apb_pprot,
    output logic [AW-1:0]        s0_apb_paddr,
    output logic [DW-1:0]        s0_apb_pwdata,
    output logic [SW-1:0]        s0_apb_pstrb,
    input  logic                 s0_apb_pready,
    input  logic [DW-1:0]        s0_apb_prdata,
    input  logic                 s0_apb_pslverr,

    output logic                 s1_apb_psel,
    output logic                 s1_apb_penable,
    output logic                 s1_apb_pwrite,
    output logic [2:0]           s1_apb_pprot,
    output logic [AW-1:0]        s1_apb_paddr,
    output logic [DW-1:0]        s1_apb_pwdata,
    output logic [SW-1:0]        s1_apb_pstrb,
    input  logic                 s1_apb_pready,
    input  logic [DW-1:0]        s1_apb_prdata,
    input  logic                 s1_apb_pslverr,

    output logic                 s2_apb_psel,
    output logic                 s2_apb_penable,
    output logic                 s2_apb_pwrite,
    output logic [2:0]           s2_apb_pprot,
    output logic [AW-1:0]        s2_apb_paddr,
    output logic [DW-1:0]        s2_apb_pwdata,
    output logic [SW-1:0]        s2_apb_pstrb,
    input  logic                 s2_apb_pready,
    input  logic [DW-1:0]        s2_apb_prdata,
    input  logic                 s2_apb_pslverr,

    output logic                 s3_apb_psel,
    output logic                 s3_apb_penable,
    output logic                 s3_apb_pwrite,
    output logic [2:0]           s3_apb_pprot,
    output logic [AW-1:0]        s3_apb_paddr,
    output logic [DW-1:0]        s3_apb_pwdata,
    output logic [SW-1:0]        s3_apb_pstrb,
    input  logic                 s3_apb_pready,
    input  logic [DW-1:0]        s3_apb_prdata,
    input  logic                 s3_apb_pslverr,

    output logic                 s4_apb_psel,
    output logic                 s4_apb_penable,
    output logic                 s4_apb_pwrite,
    output logic [2:0]           s4_apb_pprot,
    output logic [AW-1:0]        s4_apb_paddr,
    output logic [DW-1:0]        s4_apb_pwdata,
    output logic [SW-1:0]        s4_apb_pstrb,
    input  logic                 s4_apb_pready,
    input  logic [DW-1:0]        s4_apb_prdata,
    input  logic                 s4_apb_pslverr,

    output logic                 s5_apb_psel,
    output logic                 s5_apb_penable,
    output logic                 s5_apb_pwrite,
    output logic [2:0]           s5_apb_pprot,
    output logic [AW-1:0]        s5_apb_paddr,
    output logic [DW-1:0]        s5_apb_pwdata,
    output logic [SW-1:0]        s5_apb_pstrb,
    input  logic                 s5_apb_pready,
    input  logic [DW-1:0]        s5_apb_prdata,
    input  logic                 s5_apb_pslverr,

    output logic                 s6_apb_psel,
    output logic                 s6_apb_penable,
    output logic                 s6_apb_pwrite,
    output logic [2:0]           s6_apb_pprot,
    output logic [AW-1:0]        s6_apb_paddr,
    output logic [DW-1:0]        s6_apb_pwdata,
    output logic [SW-1:0]        s6_apb_pstrb,
    input  logic                 s6_apb_pready,
    input  logic [DW-1:0]        s6_apb_prdata,
    input  logic                 s6_apb_pslverr,

    output logic                 s7_apb_psel,
    output logic                 s7_apb_penable,
    output logic                 s7_apb_pwrite,
    output logic [2:0]           s7_apb_pprot,
    output logic [AW-1:0]        s7_apb_paddr,
    output logic [DW-1:0]        s7_apb_pwdata,
    output logic [SW-1:0]        s7_apb_pstrb,
    input  logic                 s7_apb_pready,
    input  logic [DW-1:0]        s7_apb_prdata,
    input  logic                 s7_apb_pslverr,

    output logic                 s8_apb_psel,
    output logic                 s8_apb_penable,
    output logic                 s8_apb_pwrite,
    output logic [2:0]           s8_apb_pprot,
    output logic [AW-1:0]        s8_apb_paddr,
    output logic [DW-1:0]        s8_apb_pwdata,
    output logic [SW-1:0]        s8_apb_pstrb,
    input  logic                 s8_apb_pready,
    input  logic [DW-1:0]        s8_apb_prdata,
    input  logic                 s8_apb_pslverr,

    output logic                 s9_apb_psel,
    output logic                 s9_apb_penable,
    output logic                 s9_apb_pwrite,
    output logic [2:0]           s9_apb_pprot,
    output logic [AW-1:0]        s9_apb_paddr,
    output logic [DW-1:0]        s9_apb_pwdata,
    output logic [SW-1:0]        s9_apb_pstrb,
    input  logic                 s9_apb_pready,
    input  logic [DW-1:0]        s9_apb_prdata,
    input  logic                 s9_apb_pslverr
);

    apb_xbar_thin #(
        .M(10),
        .S(10),
        .ADDR_WIDTH(32),
        .DATA_WIDTH(32)
    ) apb_xbar_thin_inst (
        .aclk                (aclk),
        .aresetn             (aresetn),
        .SLAVE_ENABLE        ({1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1}),
        .SLAVE_ADDR_BASE     ({32'h9000, 32'h8000, 32'h7000, 32'h6000, 32'h5000, 32'h4000, 32'h3000, 32'h2000, 32'h1000, 32'h0}),
        .SLAVE_ADDR_LIMIT    ({32'h9FFF, 32'h8FFF, 32'h7FFF, 32'h6FFF, 32'h5FFF, 32'h4FFF, 32'h3FFF, 32'h2FFF, 32'h1FFF, 32'hFFF}),
        // .SLAVE_ADDR_BASE     ({32'h0, 32'h1000, 32'h2000, 32'h3000, 32'h4000, 32'h5000, 32'h6000, 32'h7000, 32'h8000, 32'h9000}),
        // .SLAVE_ADDR_LIMIT    ({32'hFFF, 32'h1FFF, 32'h2FFF, 32'h3FFF, 32'h4FFF, 32'h5FFF, 32'h6FFF, 32'h7FFF, 32'h8FFF, 32'h9FFF}),
        .THRESHOLDS          (40'h4444444444),
        .m_apb_psel     ({m9_apb_psel, m8_apb_psel, m7_apb_psel, m6_apb_psel, m5_apb_psel, m4_apb_psel, m3_apb_psel, m2_apb_psel, m1_apb_psel, m0_apb_psel}),
        .m_apb_penable  ({m9_apb_penable, m8_apb_penable, m7_apb_penable, m6_apb_penable, m5_apb_penable, m4_apb_penable, m3_apb_penable, m2_apb_penable, m1_apb_penable, m0_apb_penable}),
        .m_apb_pwrite   ({m9_apb_pwrite, m8_apb_pwrite, m7_apb_pwrite, m6_apb_pwrite, m5_apb_pwrite, m4_apb_pwrite, m3_apb_pwrite, m2_apb_pwrite, m1_apb_pwrite, m0_apb_pwrite}),
        .m_apb_pprot    ({m9_apb_pprot, m8_apb_pprot, m7_apb_pprot, m6_apb_pprot, m5_apb_pprot, m4_apb_pprot, m3_apb_pprot, m2_apb_pprot, m1_apb_pprot, m0_apb_pprot}),
        .m_apb_paddr    ({m9_apb_paddr, m8_apb_paddr, m7_apb_paddr, m6_apb_paddr, m5_apb_paddr, m4_apb_paddr, m3_apb_paddr, m2_apb_paddr, m1_apb_paddr, m0_apb_paddr}),
        .m_apb_pwdata   ({m9_apb_pwdata, m8_apb_pwdata, m7_apb_pwdata, m6_apb_pwdata, m5_apb_pwdata, m4_apb_pwdata, m3_apb_pwdata, m2_apb_pwdata, m1_apb_pwdata, m0_apb_pwdata}),
        .m_apb_pstrb    ({m9_apb_pstrb, m8_apb_pstrb, m7_apb_pstrb, m6_apb_pstrb, m5_apb_pstrb, m4_apb_pstrb, m3_apb_pstrb, m2_apb_pstrb, m1_apb_pstrb, m0_apb_pstrb}),
        .m_apb_pready   ({m9_apb_pready, m8_apb_pready, m7_apb_pready, m6_apb_pready, m5_apb_pready, m4_apb_pready, m3_apb_pready, m2_apb_pready, m1_apb_pready, m0_apb_pready}),
        .m_apb_prdata   ({m9_apb_prdata, m8_apb_prdata, m7_apb_prdata, m6_apb_prdata, m5_apb_prdata, m4_apb_prdata, m3_apb_prdata, m2_apb_prdata, m1_apb_prdata, m0_apb_prdata}),
        .m_apb_pslverr  ({m9_apb_pslverr, m8_apb_pslverr, m7_apb_pslverr, m6_apb_pslverr, m5_apb_pslverr, m4_apb_pslverr, m3_apb_pslverr, m2_apb_pslverr, m1_apb_pslverr, m0_apb_pslverr}),
        .s_apb_psel     ({s9_apb_psel, s8_apb_psel, s7_apb_psel, s6_apb_psel, s5_apb_psel, s4_apb_psel, s3_apb_psel, s2_apb_psel, s1_apb_psel, s0_apb_psel}),
        .s_apb_penable  ({s9_apb_penable, s8_apb_penable, s7_apb_penable, s6_apb_penable, s5_apb_penable, s4_apb_penable, s3_apb_penable, s2_apb_penable, s1_apb_penable, s0_apb_penable}),
        .s_apb_pwrite   ({s9_apb_pwrite, s8_apb_pwrite, s7_apb_pwrite, s6_apb_pwrite, s5_apb_pwrite, s4_apb_pwrite, s3_apb_pwrite, s2_apb_pwrite, s1_apb_pwrite, s0_apb_pwrite}),
        .s_apb_pprot    ({s9_apb_pprot, s8_apb_pprot, s7_apb_pprot, s6_apb_pprot, s5_apb_pprot, s4_apb_pprot, s3_apb_pprot, s2_apb_pprot, s1_apb_pprot, s0_apb_pprot}),
        .s_apb_paddr    ({s9_apb_paddr, s8_apb_paddr, s7_apb_paddr, s6_apb_paddr, s5_apb_paddr, s4_apb_paddr, s3_apb_paddr, s2_apb_paddr, s1_apb_paddr, s0_apb_paddr}),
        .s_apb_pwdata   ({s9_apb_pwdata, s8_apb_pwdata, s7_apb_pwdata, s6_apb_pwdata, s5_apb_pwdata, s4_apb_pwdata, s3_apb_pwdata, s2_apb_pwdata, s1_apb_pwdata, s0_apb_pwdata}),
        .s_apb_pstrb    ({s9_apb_pstrb, s8_apb_pstrb, s7_apb_pstrb, s6_apb_pstrb, s5_apb_pstrb, s4_apb_pstrb, s3_apb_pstrb, s2_apb_pstrb, s1_apb_pstrb, s0_apb_pstrb}),
        .s_apb_pready   ({s9_apb_pready, s8_apb_pready, s7_apb_pready, s6_apb_pready, s5_apb_pready, s4_apb_pready, s3_apb_pready, s2_apb_pready, s1_apb_pready, s0_apb_pready}),
        .s_apb_prdata   ({s9_apb_prdata, s8_apb_prdata, s7_apb_prdata, s6_apb_prdata, s5_apb_prdata, s4_apb_prdata, s3_apb_prdata, s2_apb_prdata, s1_apb_prdata, s0_apb_prdata}),
        .s_apb_pslverr  ({s9_apb_pslverr, s8_apb_pslverr, s7_apb_pslverr, s6_apb_pslverr, s5_apb_pslverr, s4_apb_pslverr, s3_apb_pslverr, s2_apb_pslverr, s1_apb_pslverr, s0_apb_pslverr})
    );

endmodule : apb_xbar_thin_wrap_m10_s10
