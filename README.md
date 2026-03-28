# RTL Formal Verification — 1011 Sequence Detector

Bitwise overlapping sequence detector built in SystemVerilog with a full FPV environment using VC Formal.

## What this project does

Detects the pattern `1011` in a continuous bit stream. "Overlapping" means the tail of one match can be the head of the next — the FSM handles this without missing a beat.

Formal verification proves correctness for **all possible inputs** — not just test cases.

## Project structure
## Run it
```bash
cat > ~/seq_detector/README.md << 'EOF'
# RTL Formal Verification — 1011 Sequence Detector

Bitwise overlapping sequence detector built in SystemVerilog with a full FPV environment using VC Formal.

## What this project does

Detects the pattern `1011` in a continuous bit stream. "Overlapping" means the tail of one match can be the head of the next — the FSM handles this without missing a beat.

Formal verification proves correctness for **all possible inputs** — not just test cases.

## Project structure
```
rtl/   seq_detector.sv        — 5-state FSM design
fpv/   seq_detector_props.sv  — SVA assertions (safety, liveness, deadlock, cover)
       fpv_env.sv             — bind statement, attaches properties to design
       run_fpv.tcl            — VC Formal automation script
tb/    tb_seq_detector.sv     — simulation testbench (Icarus Verilog)
sim/   simulate.py            — Python FSM simulation, no tools needed
```

## Run it
```bash
# Python simulation (no tools needed)
python3 sim/simulate.py

# SystemVerilog simulation
iverilog -g2012 -o sim.out tb/tb_seq_detector.sv rtl/seq_detector.sv
vvp sim.out

# Formal verification (requires VC Formal)
cd fpv && vcf -f run_fpv.tcl
```

## Properties proved

| Property | Type | Proves |
|---|---|---|
| `p_no_false_detect` | Safety | `detected` only HIGH in S4 |
| `p_detected_single_cycle` | Safety | `detected` never HIGH two cycles in a row |
| `p_valid_state` | Safety | FSM never enters undefined state |
| `p_reset_lands_S0` | Safety | Reset always returns to IDLE |
| `p_S4_only_via_S3` | Safety | Match only reachable via correct sequence |
| `p_detect_1011` | Liveness | Pattern `1011` always causes detection |
| `p_S0–S4_no_deadlock` | Deadlock | Every state has a valid successor |
| `c_detection_reachable` | Cover | Detected state is reachable |
| `c_double_detection` | Cover | Overlapping detection is possible |
