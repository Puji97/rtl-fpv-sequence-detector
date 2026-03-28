`timescale 1ns/1ps

module tb_seq_detector;

    logic clk, rst_n, in, detected;

    seq_detector dut (
        .clk(clk), .rst_n(rst_n), .in(in), .detected(detected)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    task reset_dut();
        rst_n = 0; in = 0;
        repeat(3) @(posedge clk);
        @(negedge clk); rst_n = 1;
        @(posedge clk); #1;
        $display("  [reset] state=%b", dut.current_state);
    endtask

    task apply_bit(input logic b, input string label);
        @(negedge clk); in = b;
        @(posedge clk); #2;
        $display("  %s | in=%b | state=%b | detected=%b",
                  label, b, dut.current_state, detected);
    endtask

    initial begin
        $dumpfile("waves.vcd");
        $dumpvars(0, tb_seq_detector);

        $display("\n=== TEST 1: Basic 1011 — expect detected on last bit ===");
        reset_dut();
        apply_bit(1,"bit1"); apply_bit(0,"bit2");
        apply_bit(1,"bit3"); apply_bit(1,"bit4");

        $display("\n=== TEST 2: Wrong pattern 1010 — expect no detection ===");
        reset_dut();
        apply_bit(1,"bit1"); apply_bit(0,"bit2");
        apply_bit(1,"bit3"); apply_bit(0,"bit4");

        $display("\n=== TEST 3: Overlapping 10111011 — expect detected TWICE ===");
        reset_dut();
        apply_bit(1,"b1"); apply_bit(0,"b2");
        apply_bit(1,"b3"); apply_bit(1,"b4");
        apply_bit(1,"b5"); apply_bit(0,"b6");
        apply_bit(1,"b7"); apply_bit(1,"b8");

        $display("\n=== TEST 4: Noisy 0001011 — expect detected once at end ===");
        reset_dut();
        apply_bit(0,"b1"); apply_bit(0,"b2"); apply_bit(0,"b3");
        apply_bit(1,"b4"); apply_bit(0,"b5");
        apply_bit(1,"b6"); apply_bit(1,"b7");

        $display("\nDone. Run: gtkwave waves.vcd");
        $finish;
    end

endmodule
