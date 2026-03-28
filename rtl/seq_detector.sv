module seq_detector (
    input  logic clk,
    input  logic rst_n,
    input  logic in,
    output logic detected
);

    typedef enum logic [2:0] {
        S0 = 3'b000,
        S1 = 3'b001,
        S2 = 3'b010,
        S3 = 3'b011,
        S4 = 3'b100
    } state_t;

    state_t current_state, next_state;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            current_state <= S0;
        else
            current_state <= next_state;
    end

    always_comb begin
        next_state = S0;
        detected   = 1'b0;

        case (current_state)
            S0: if (in) next_state = S1; else next_state = S0;
            S1: if (!in) next_state = S2; else next_state = S1;
            S2: if (in)  next_state = S3; else next_state = S0;
            S3: begin
                if (in) begin
                    next_state = S4;
                    detected   = 1'b1;
                end else next_state = S2;
            end
            S4: if (in) next_state = S1; else next_state = S2;
            default: next_state = S0;
        endcase
    end

endmodule
