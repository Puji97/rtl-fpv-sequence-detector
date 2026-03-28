analyze -sv12 ../rtl/seq_detector.sv
analyze -sv12 ../fpv/seq_detector_props.sv
analyze -sv12 ../fpv/fpv_env.sv

elaborate -top seq_detector

clock clk -period 10
reset -expression {!rst_n}

set_prove_time_limit 3600
prove -all
report -summary
report -file fpv_results.txt
