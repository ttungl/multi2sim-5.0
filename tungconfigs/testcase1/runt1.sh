#!/bin/bash
# NOC128/cores16/MC4/freq3.0/L2size512/L2assoc8/pipelinewidth4/L1size32/ROB128/bimod4096/bpred1024/fft/
#note: first run "chmod a+x file.sh"

m2s --x86-sim detailed --x86-report tungconfigs/testcase1/pipeline_mm_mult_serial.out --mem-report tungconfigs/testcase1/mem_mm_mult_serial.out --x86-config tungconfigs/testcase1/x86_cpuconfig --net-config tungconfigs/testcase1/netconfig --net-max-cycles 1000000 --mem-config tungconfigs/testcase1/memconfig --x86-max-inst 1000 --net-report report_mm_mult_serial_8_netrunt1 ./mm_mult_serial/mm_mult_serial 8 

# Stand-alone Interconnection Network
# m2s --net-config tungconfigs/testcase1/netconfig --net-sim net0 --net-max-cycles 1000000 --net-report report-net ./mm_mult_serial/mm_mult_serial 8

# m2s --net-config netconfig --net-sim mynet --net-max-cycles 1000000 --report-net report-net --net-injection-rate 0.1