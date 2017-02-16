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

# Functions' Arguments:
	# create_cpuconfig(num_of_cores, num_of_threads, ROB_size, pipelines_size, bimod_size, BTB_Sets, BTB_Assoc);
	# create_evergreen_gpuconfig(num_of_cores);

# ==========================================================

# from file import function
# from caches_latency_calculation import calculate_caches_latency
from create_cpu_config import create_cpuconfig
from create_evergreen_gpuconfig import create_evergreen_gpuconfig
from create_southern_islands_gpuconfig import create_southern_islands_gpuconfig
from create_memconfig import create_memconfig
from create_netconfig import create_netconfig

# [cpu gpu mc]
# [16 16 4] : 16 nodes
# [48 96 16] : 64 nodes
## CPU Parameters
num_of_cpu_cores = 16; 
cpu_frequency = 3500; ## 3.5GHz
num_of_threads = 1;
ROB_size = 128;
pipelines_size = 4;
bimod_size = 4*1024;
bpred_size = 1*1024;

## GPU Parameters
num_of_gpu_cores = 16; ## the number of compute units of GPUs. (each GPU has 4 units.)
type_of_gpu_model = 2; ## [1]: evergreen; [2]: southern islands

## CPU Memory Parameters 	
num_of_MC = 4 			# number of memory controllers; [2, 4, 8]
L1_Inst_shared = 0		# enable/disable (1/0) shared Instruction L1$
L1_size = 32			# size of L1$ (kB); [16, 32, 64]
L1_assoc = 1			# associativity of L1$ (#-way) full-assoc
L2_size = 512			# size of L2$ (kB); [256, 512, 1024]
L2_assoc = 8			# associativity of L2$ (#-way); [4, 8, 16]
L1_latency = 1			# latency of L1$ (cycles)
L2_latency = 4			# latency of L2$ (cycles)
L1_blocksize = 64		# blocksize of L1$ (Bytes)
L2_blocksize = 64		# blocksize of L2$ (Bytes)
Memory_latency = 100	# latency of DRAM main memory

## GPU Memory Parameters (iiswc16: Victor Garcia)	
GPU_L1_size = 64		# size of L1$ (kB)
GPU_L1_assoc = 4		# associativity of L1$ (kB)
GPU_L2_size = 512		# size of L2$ (kB)
GPU_L2_assoc = 16		# associativity of L2$ (kB)
GPU_L1_latency = 22 	# latency of L1$ (ns)
GPU_L2_latency = 63 	# latency of L2$ (ns)
GPU_L1_blocksize = 64 	# blocksize of L1$ (Bytes)
GPU_L2_blocksize = 64 	# blocksize of L2$ (Bytes) 

## Network Parameters
#### Notice: source-destination nodes' id from the input files should start at 1, not zero.
LOCALLINKS_PATH = 'results_hybrid_local_links/test_topoA_hybridlinks_4x4.txt'
HYBRIDLINKS_PATH = 'results_hybrid_local_links/test_topoA_locallinks_4x4.txt'
## network_mode: [0] default 2D-mesh; [1]: Customized 2D-Mesh Network; [2]: Torus; [3]: Ring
network_mode = 1

## main()
def main():
	# Caches and memory latency calculation for memconfig
	#### for now, user will manually run CACTI to obtain and update these parameters.

	# Methods for creating the configuration files
	create_cpuconfig(num_of_cpu_cores, cpu_frequency, num_of_threads, ROB_size, pipelines_size, bimod_size, bpred_size);

	if type_of_gpu_model == 1:
		create_evergreen_gpuconfig(num_of_gpu_cores);
	if type_of_gpu_model == 2:
		create_southern_islands_gpuconfig(num_of_gpu_cores);

	num_nodes = create_memconfig(num_of_cpu_cores, \
								num_of_gpu_cores, \
								type_of_gpu_model, \
								num_of_MC, \
								L1_Inst_shared, \
								L1_size, \
								L1_assoc, \
								L2_size, \
								L2_assoc, \
								L1_latency, \
								L2_latency, \
								L1_blocksize, \
								L2_blocksize, \
								Memory_latency, \
								GPU_L1_size, \
								GPU_L1_assoc, \
								GPU_L2_size, \
								GPU_L2_assoc, \
								GPU_L1_latency, \
								GPU_L2_latency, \
								GPU_L1_blocksize, \
								GPU_L2_blocksize);

	create_netconfig(num_nodes, L2_blocksize, network_mode, LOCALLINKS_PATH, HYBRIDLINKS_PATH)

if __name__ == "__main__": main()
