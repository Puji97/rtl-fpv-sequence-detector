module seq_detector_props (
    input logic clk,
    input logic rst_n,
    input logic in,
    input logic detected,
    input logic [2:0] current_state
);

    default clocking @(posedge clk); endclocking
    default disable iff (!rst_n);

    // Safety 1: detected only when in state S4
    p_no_false_detect: assert property (
        detected |-> (current_state == 3'b100)
    );

    // Safety 2: detected never high two cycles in a row
    p_detected_single_cycle: assert property (
        detected |=> !detected
    );

    // Safety 3: state always valid
    p_valid_state: assert property (
        current_state inside {3'b000,3'b001,3'b010,3'b011,3'b100}
    );

    // Safety 4: reset returns to S0
    p_reset_lands_S0: assert property (
        $fell(rst_n) |=> (current_state == 3'b000)
    );

    // Safety 5: S4 only reachable from S3 with in=1
    p_S4_only_via_S3: assert property (
        (current_state == 3'b100) |->
        ($past(current_state) == 3'b011 && $past(in) == 1'b1)
    );

    // Liveness: pattern 1011 always causes detection
    p_detect_1011: assert property (
        (in == 1'b1) ##1 (in == 1'b0)
        ##1 (in == 1'b1) ##1 (in == 1'b1)
        |-> detected
    );

    // Deadlock checks: every state has a valid successor
    p_S0_no_deadlock: assert property (
        (current_state == 3'b000) |=>
        (current_state == 3'b000 || current_state == 3'b001)
    );
    p_S1_no_deadlock: assert property (
        (current_state == 3'b001) |=>
        (current_state == 3'b001 || current_state == 3'b010)
    );
    p_S2_no_deadlock: assert property (
        (current_state == 3'b010) |=>
        (current_state == 3'b000 || current_state == 3'b011)
    );
    p_S3_no_deadlock: assert property (
        (current_state == 3'b011) |=>
        (current_state == 3'b010 || current_state == 3'b100)
    );
    p_S4_no_deadlock: assert property (
        (current_state == 3'b100) |=>
        (current_state == 3'b001 || current_state == 3'b010)
    );

    // Cover: prove these situations are reachable
    c_detection_reachable:  cover property (detected);
    c_reach_S0: cover property (current_state == 3'b000);
    c_reach_S1: cover property (current_state == 3'b001);
    c_reach_S2: cover property (current_state == 3'b010);
    c_reach_S3: cover property (current_state == 3'b011);
    c_reach_S4: cover property (current_state == 3'b100);
    c_double_detection: cover property (detected ##[1:8] detected);

endmodule
