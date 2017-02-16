# ==========================================================
# Copyright 2017 `Tung Thanh Le` 
# Email: ttungl at gmail dot com
#
# Simulation Configuration Files Generator for Multi2Sim
# (aka, `GenSimConfigM2S`)
# `GenSimConfigM2S` is free software, which is freely to be
# redistributed and modified it under the terms of 
# the GNU General Public License as published by
# the Free Software Foundation. 
# For more details `http://www.gnu.org/licenses`
# `GenSimConfigM2S` is written to help you configure M2S 
# easily, but non-warranty and non-mechantability.
# ==========================================================

# Description: This generates `memconfig` file for M2S
# Each core has its own Instruction-L1$ and Data-L1$.
# ==========================================================

def create_memconfig( 	num_of_CPU_cores, 	# number of CPU cores
						num_of_GPU_cores,	# number of GPU cores
						num_of_MC, 		# number of memory controllers
						L1_size,		# size of L1$ (kB)
						L1_assoc,		# associativity of L1$ (#-way) 
						L2_size,		# size of L2$ (kB)
						L2_assoc,		# associativity of L2$ (#-way)
						L1_latency,		# latency of L1$ (cycles)
						L2_latency,		# latency of L2$ (cycles)
						L1_blocksize,	# blocksize of L1$ (Bytes)
						L2_blocksize,	# blocksize of L2$ (Bytes)
						Memory_latency, # latency of DRAM main memory
						GPU_L1_size,	# size of L1$ (kB)
						GPU_L1_assoc,	# associativity of L1$ (kB)
						GPU_L2_size,	# size of L2$ (kB)
						GPU_L2_assoc,	# associativity of L2$ (kB)
						GPU_L1_latency, # latency of L1$ (cycles)
						GPU_L2_latency, # latency of L2$ (cycles)
						GPU_L1_blocksize, # blocksize of L1$ (Bytes)
						GPU_L2_blocksize):# blocksize of L2$ (Bytes) 
	# check input validation
	assert (num_of_CPU_cores>=4), "Error! Number of CPU cores must be at least 4; range [4,8,16,32,64];"
	assert (num_of_GPU_cores>=4), "Error! Number of compute units in GPU must be at least 4; range [4,8,16,32,64];"
	
	# bandwidth and buffer size
	bandwidth = L2_blocksize + 8;
	bufferSize = bandwidth * 16;

	# File name
	f = open('memconfig', 'w');

	# Data cache (D-L1)
	count_L2_cache_inc = 0;
	L2_cache_inc = 0;
	for i in range(num_of_CPU_cores):
		## increase
		count_L2_cache_inc = count_L2_cache_inc + 1;
		## to_file
		f.write("[Module mod-cpu-dl1-%0.f]\n" % i);
		f.write("Type = Cache\n");
		f.write("Geometry = geo-cpu-d-l1\n");
		f.write("LowNetwork = net-l1-l2-%0.f\n" % L2_cache_inc);
		f.write("LowNetworkNode = mod-l2-%0.f\n" % L2_cache_inc);
		f.write("\n");
		## check increasing and reset
		if count_L2_cache_inc==2:
			count_L2_cache_inc = 0; # reset
			L2_cache_inc = L2_cache_inc + 1;

	# Instruction cache (I-L1)
	## Note: if I-L1 is shared, (#cores/2) instead #cores.
	count_L2_cache_inc = 0;
	L2_cache_inc = 0;
	for i in range(num_of_CPU_cores):
		## increase
		count_L2_cache_inc = count_L2_cache_inc + 1;
		## to_file
		f.write("[Module mod-cpu-il1-%0.f]\n" % i);
		f.write("Type = Cache\n");
		f.write("Geometry = geo-cpu-i-l1\n");
		f.write("LowNetwork = net-l1-l2-%0.f\n" % L2_cache_inc);
		f.write("LowNetworkNode = mod-l2-%0.f\n" % L2_cache_inc);
		f.write("\n");
		## check increasing and reset
		if count_L2_cache_inc==2:
			count_L2_cache_inc = 0; # reset
			L2_cache_inc = L2_cache_inc + 1;

	# Network CPU L1$-L2$
	count_L2_cache_inc = 0;
	L2_cache_inc = 0;
	for i in range(num_of_CPU_cores):
		if count_L2_cache_inc%2 == 0:
			f.write("[Network net-cpu-l1-l2-%0.f]\n" % L2_cache_inc);
			f.write("DefaultInputBufferSize = %0.f\n" % bufferSize);
			f.write("DefaultOutputBufferSize = %0.f\n" % bufferSize);
			f.write("DefaultBandwidth = %0.f\n" % bandwidth);
			f.write("\n");
			L2_cache_inc = L2_cache_inc + 1;
		# counting
		count_L2_cache_inc = count_L2_cache_inc + 1;	
	
	# L2$ to memory
	## LowModules
	LowModules_MM = "LowModules =";
	for i in range(num_of_MC):
		LowModules_MM = LowModules_MM + " mod-cpu-mm-%0.f" % i;
	##
	count_L2_MM_inc = 0;
	L2_cache_inc = 0;
	for i in range(num_of_CPU_cores):
		if count_L2_MM_inc%2 == 0:
			f.write("[Module mod-cpu-l2-%0.f]\n" % L2_cache_inc);
			f.write("Type = Cache\n");
			f.write("Geometry = geo-cpu-l2\n");
			f.write("HighNetwork = net-l1-l2-%0.f\n" % L2_cache_inc);
			f.write("LowNetwork = net0\n");
			f.write("LowNetworkNode = n%0.f\n" % L2_cache_inc);
			f.write("%s\n" % LowModules_MM);
			f.write("\n");
			L2_cache_inc = L2_cache_inc + 1;
		# counting
		count_L2_MM_inc = count_L2_MM_inc + 1;	
	
	# Memory
	Node_MM_increase = 0;
	for i in range(num_of_MC):
		Node_MM_increase = (L2_cache_inc+i);
		f.write("[Module mod-cpu-mm-%0.f]\n" % i);
		f.write("Type = MainMemory\n");
		f.write("BlockSize = %0.f\n" % L2_blocksize);
		f.write("Latency = %0.f\n" % Memory_latency);
		f.write("Ports = 1\n");
		f.write("HighNetwork = net0\n");
		f.write("HighNetworkNode = n%0.f\n" % Node_MM_increase);
		f.write("AddressRange = ADDR DIV %0.f MOD %0.f EQ %0.f\n" % (L2_blocksize, num_of_MC, i) );
		f.write("\n");

	# CPU cores 
	for i in range(num_of_CPU_cores):
		f.write("[Entry core-%0.f]\n" % i);
		f.write("Arch = x86\n");
		f.write("Core = %0.f\n" % i);
		f.write("Thread = 0\n");
		f.write("DataModule = mod-cpu-dl1-%0.f\n" % i);
		f.write("InstModule = mod-cpu-il1-%0.f\n" % i);
		f.write("\n");

	# Cache Geometry I-L1$
	f.write("[CacheGeometry geo-cpu-i-l1]\n");
	f.write("Sets = %0.f\n" % (L1_size*1024/L1_assoc/L1_blocksize));
	f.write("Assoc = %0.f\n" % L1_assoc);
	f.write("BlockSize = %0.f\n" % L1_blocksize);
	f.write("Latency = %0.f\n" % L1_latency);
	f.write("Policy = LRU\n");
	f.write("Ports = 1\n");
	f.write("\n");

	# Cache Geometry D-L1$
	f.write("[CacheGeometry geo-cpu-d-l1]\n");
	f.write("Sets = %0.f\n" % (L1_size*1024/L1_assoc/L1_blocksize));
	f.write("Assoc = %0.f\n" % L1_assoc);
	f.write("BlockSize = %0.f\n" % L1_blocksize);
	f.write("Latency = %0.f\n" % L1_latency);
	f.write("Policy = LRU\n");
	f.write("Ports = 1\n");
	f.write("\n");

	# Cache Geometry L2
	f.write("[CacheGeometry geo-cpu-l2]\n");
	f.write("Sets = %0.f\n" % (L2_size*1024/L2_blocksize/L2_assoc));
	f.write("Assoc = %0.f\n" % L2_assoc);
	f.write("BlockSize = %0.f\n" % L2_blocksize);
	f.write("Latency = %0.f\n" % L2_latency);
	f.write("Policy = LRU\n");
	f.write("Ports = 1\n");
	f.write("\n");

	###################################################################

	# Mem-GPU-cores
	## GPU-L1$
	## Each L1$ is for two compute units.
	## Each GPU has 4 compute units.
	count_L1_gpu_inc = 0;
	L1_gpu_cache_inc = 0;
	for i in range(num_of_GPU_cores/2): # num of compute units
		## increase
		count_L1_gpu_inc = count_L1_gpu_inc + 1;
		f.write("[Module mod-gpu-l1-%0.f]\n" % i);
		f.write("Type = Cache\n");
		f.write("Geometry = geo-gpu-l1\n");
		f.write("LowNetwork = net-gpu-l1-l2-%0.f\n" % L1_gpu_cache_inc);
		f.write("LowModules = mod-gpu-l2-%0.f\n" % L1_gpu_cache_inc);
		f.write("\n");	
		## check increasing and reset
		if count_L1_gpu_inc%2==0:
			count_L1_gpu_inc = 0; # reset
			L1_gpu_cache_inc = L1_gpu_cache_inc + 1;

	## GPU-L2$
	## Each L2$ is for two L1$.
	## Four CUs on one L2$.
		## L2$ to memory
		## LowModules
	LowModules_gpu_MM = "LowModules =";
	for i in range(num_of_GPU_cores/4): # number of MC # num of compute units.
		LowModules_gpu_MM = LowModules_gpu_MM + " mod-gpu-mm-%0.f" % i;

	Node_L2MM_GPU_increase = Node_MM_increase;	
	for i in range(num_of_GPU_cores/4):
		Node_L2MM_GPU_increase = Node_L2MM_GPU_increase + 1;
		f.write("[Module mod-gpu-l2-%0.f]\n" % i);
		f.write("Type = Cache\n");
		f.write("Geometry = geo-gpu-l2\n");
		f.write("HighNetwork = net-gpu-l1-l2-%0.f\n" % i);
		f.write("LowNetwork = net0\n");
		f.write("LowNetworkNode = n%0.f\n" % Node_L2MM_GPU_increase);
		f.write("%s\n" % LowModules_gpu_MM);
		f.write("\n");

	# GPU Main memory
	Node_L2_MM_GPU_increase = Node_L2MM_GPU_increase
	for i in range(num_of_GPU_cores/4):
		Node_L2_MM_GPU_increase = Node_L2_MM_GPU_increase + 1;
		f.write("[Module mod-gpu-mm-%0.f]\n" % i);
		f.write("Type = MainMemory\n");
		f.write("BlockSize = %0.f\n" % L2_blocksize);
		f.write("Latency = %0.f\n" % Memory_latency);
		f.write("Ports = 1\n");
		f.write("HighNetwork = net0\n");
		f.write("HighNetworkNode = n%0.f\n" % Node_L2_MM_GPU_increase);
		# f.write("AddressRange = ADDR DIV %0.f MOD %0.f EQ %0.f\n" % (L2_blocksize, num_of_MC, i) );
		f.write("\n");

	# Network-CPU	
	count_L2_cache_inc1 = 0;
	L2_cache_inc1 = 0;
	for i in range(num_of_GPU_cores):
		if count_L2_cache_inc1%4 == 0:
			f.write("[Network net-gpu-l1-l2-%0.f]\n" % L2_cache_inc1);
			f.write("DefaultInputBufferSize = %0.f\n" % bufferSize);
			f.write("DefaultOutputBufferSize = %0.f\n" % bufferSize);
			f.write("DefaultBandwidth = %0.f\n" % bandwidth);
			f.write("\n");
			L2_cache_inc1 = L2_cache_inc1 + 1;
		# counting
		count_L2_cache_inc1 = count_L2_cache_inc1 + 1;

	# GPU cores
	count_L1_gpu_inc1 = 0;
	L1_gpu_cache_inc1 = 0;
	for i in range(num_of_GPU_cores):
		count_L1_gpu_inc1 = count_L1_gpu_inc1 + 1;
		f.write("[Entry gpu-cu-%0.f]\n" % i);
		f.write("Arch = Evergreen\n");
		f.write("ComputeUnit = %0.f\n" % i);
		f.write("Module = mod-gpu-l1-%0.f\n" % L1_gpu_cache_inc1);
		f.write("\n");
		## check increasing and reset
		if count_L1_gpu_inc1%2==0:
			count_L1_gpu_inc1 = 0; # reset
			L1_gpu_cache_inc1 = L1_gpu_cache_inc1 + 1;


	# Cache Geometry GPU L1$
	f.write("[CacheGeometry geo-gpu-l1]\n");
	f.write("Sets = %0.f\n" % (GPU_L1_size*1024/GPU_L1_blocksize/GPU_L1_assoc));
	f.write("Assoc = %0.f\n" % GPU_L1_assoc);
	f.write("BlockSize = %0.f\n" % GPU_L1_blocksize);
	f.write("Latency = %0.f\n" % GPU_L1_latency);
	f.write("Policy = LRU\n");
	f.write("Ports = 1\n");
	f.write("\n");


	# Cache Geometry GPU L2$
	f.write("[CacheGeometry geo-gpu-l2]\n");
	f.write("Sets = %0.f\n" % (GPU_L2_size*1024/GPU_L2_blocksize/GPU_L2_assoc));
	f.write("Assoc = %0.f\n" % GPU_L2_assoc);
	f.write("BlockSize = %0.f\n" % GPU_L2_blocksize);
	f.write("Latency = %0.f\n" % GPU_L2_latency);
	f.write("Policy = LRU\n");
	f.write("Ports = 1\n");
	f.write("\n");

	# close
	f.close();



# method call
create_memconfig(8,8,4,32,4,512,8,1,4,64,64,100,64,4,512,16,22,63,128,128);
	

