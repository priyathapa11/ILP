import m5
from m5.objects import *

# Create the system
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'  # Use timing memory mode for detailed timing simulation
system.mem_ranges = [AddrRange('512MB')]  # Address range for memory

# Create CPU
system.cpu = O3CPU()
system.cpu.numThreads = 2

# Configure it to be superscalar by increasing widths
system.cpu.fetchWidth = 4
system.cpu.decodeWidth = 4
system.cpu.renameWidth = 4
system.cpu.dispatchWidth = 4
system.cpu.issueWidth = 4
system.cpu.wbWidth = 4
system.cpu.commitWidth = 4
system.cpu.squashWidth = 4

# Create memory bus
system.membus = SystemXBar()
system.system_port = system.membus.cpu_side_ports  # Connect system port to membus

# Connect CPU icache and dcache ports to memory bus
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# Interrupt controller setup (required for x86 SE-mode CPUs)
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Setup workload - statically linked binary
system.workload = SEWorkload.init_compatible('./intBench')
process1 = Process()
process1.cmd = ['./intBench']

system.workload = SEWorkload.init_compatible('./floatBench')
process2 = Process()
process2.cmd = ['./floatBench']

system.cpu.workload = [process1, process2]
system.cpu.createThreads()

# Create root and instantiate system
root = Root(full_system=False, system=system)
m5.instantiate()

print("Starting simulation...")
exit_event = m5.simulate()

print(f"Simulation ended at tick {m5.curTick()} because: {exit_event.getCause()}")

# Dump stats to stats.txt
m5.stats.dump()
m5.stats.reset()
