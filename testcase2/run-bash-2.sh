m2s --x86-sim detailed \
--x86-report tungconfigs/testcase2/results/pipeline_test2_mcpat_020417.out \
--mem-report tungconfigs/testcase2/results/mem_test2_mcpat_020417.out \
--x86-config ./tungconfigs/testcase2/configs/x86_cpuconfig \
--si-sim detailed \
--si-config ./tungconfigs/testcase2/configs/sigpuconfig \
--mem-config ./tungconfigs/testcase2/configs/memconfig \
--net-config ./tungconfigs/testcase2/configs/netconfig \
--x86-max-inst 100000000 \
--net-report net_test2_mcpat_020417.out \
benchmarks/m2s-bench-splash2/fft/fft -m18 -p8 -n65536 -l4