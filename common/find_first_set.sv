`timescale 1ns / 1ps

module find_first_set
#(parameter      int WIDTH = 32,
  localparameter int N = $clog2(WIDTH))
(
    input  logic [WIDTH-1:0]   data,
    output logic [N-1:0]       first_set_index
);

    function automatic logic [N-1:0] ffs(input logic [WIDTH-1:0] vector);
        logic [N-1:0] location;

        location = '{N{1'b1}};

        for (int i = 0; i < CLIENTS; i++)
            if (vector[i] == 1'b1)
                location = i[N-1:0];

        return {location};
    endfunction

    first_set_index = ffs(data);

endmodule : find_first_set