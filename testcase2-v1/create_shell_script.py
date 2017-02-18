#!/usr/bin/env python
# ===========================================================================
# Copyright 2017 `Tung Thanh Le` 
# Email: ttungl at gmail dot com
#
# Heterogeneous Architecture Configurations Generator for Multi2Sim simulator
# (aka, `HeteroArchGen4M2S`)
# `HeteroArchGen4M2S` is free software, which is freely to be
# redistributed and modified it under the terms of 
# the GNU General Public License as published by
# the Free Software Foundation. 
# For more details `http://www.gnu.org/licenses`
# `HeteroArchGen4M2S` is written to help you configure M2S 
# easily, but non-warranty and non-mechantability.
# ============================================================================
import os ## for chmod
import stat

def create_shell_script(num_CPU, num_GPU, gpu_type, max_inst, benchmark, injection_rate):
	## check benchmark
	# if benchmark == '':
	# 	benchmark = 'default_mm'

	## create a shell script in runsimulations folder.
	# File name
	f = open('run_simulation_files/run-sim-%0.f-CPU-%0.f-%s-GPU-benchmark-%s.sh' % (num_CPU, num_GPU, gpu_type, benchmark), 'w');
	## content
	f.write('m2s --x86-sim detailed ')
	f.write('--x86-report tungconfigs/testcase2/results/%s_pipeline.out ' % benchmark)
	f.write('--mem-report tungconfigs/testcase2/results/%s_mem.out ' % benchmark)
	f.write('--x86-config ./tungconfigs/testcase2/configs/x86_cpuconfig ')
	f.write('--si-sim detailed ')
	f.write('--si-config ./tungconfigs/testcase2/configs/si_gpuconfig ')
	f.write('--mem-config ./tungconfigs/testcase2/configs/memconfig ')
	f.write('--net-config ./tungconfigs/testcase2/configs/netconfig ')
	f.write('--x86-max-inst %0.f ' % max_inst)
	## network report: 
	##### Note: This file is generated under m2s directory.
	f.write('--net-report %s_netreport ' % benchmark)
	## benchmarks
	if benchmark == 'fft':
		f.write('benchmarks/m2s-bench-splash2/fft/fft -m18 -p8 -n65536 -l4')
	else:
		f.write('mm_multi_serial 8')


	## close
	f.close()

	## granted `chmod +x` for this file
	st = os.stat('run_simulation_files/run-sim-%0.f-CPU-%0.f-%s-GPU-benchmark-%s.sh' % (num_CPU, num_GPU, gpu_type, benchmark))
	os.chmod('run_simulation_files/run-sim-%0.f-CPU-%0.f-%s-GPU-benchmark-%s.sh' % (num_CPU, num_GPU, gpu_type, benchmark), st.st_mode | stat.S_IEXEC)

## tested
# create_shell_script(16, 16, 1, 10000000, 'fft', 0)
