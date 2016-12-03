#!/bin/bash
#note: first run "chmod a+x file.sh"

# m2s --x86-sim detailed --x86-report tungconfigs/testcase1/pipeline.out --mem-report tungconfigs/testcase1/mem.out --x86-config tungconfigs/testcase1/x86_cpuconfig --net-config tungconfigs/testcase1/netconfig --net-max-cycles 1000000 --mem-config tungconfigs/testcase1/memconfig --x86-max-inst 1000 --net-report report-net012 --net-injection-rate 0.1


m2s --x86-config tungconfigs/testcase1/x86_cpuconfig \
--mem-config tungconfigs/testcase1/memconfig \
--net-config tungconfigs/testcase1/netconfig \
--net-sim net0 --net-max-cycles 1000000 \
--net-report report-netrunt12_SyncIR_06 \
--net-injection-rate 0.6