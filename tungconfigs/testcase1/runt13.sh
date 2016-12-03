#!/bin/bash
#note: first run "chmod a+x file.sh"

# m2s --x86-sim detailed --x86-report tungconfigs/testcase1/pipeline.out --mem-report tungconfigs/testcase1/mem.out --x86-config tungconfigs/testcase1/x86_cpuconfig --net-config tungconfigs/testcase1/netconfig --net-max-cycles 2000000 --mem-config tungconfigs/testcase1/memconfig --x86-max-inst 1000 --net-report report-net013 --net-injection-rate 0.2


m2s --x86-config tungconfigs/testcase1/x86_cpuconfig --mem-config tungconfigs/testcase1/memconfig --net-config tungconfigs/testcase1/netconfig --net-sim net0 --net-max-cycles 1000000 --net-report report-netrunt13-splash2-ocean-p16 ./m2s-bench-splash2/ocean/ocean.i386 -n130 -p16 -e1e-07 -r20000 -t28800