import m5
from m5.objects import *

# Create the system
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Create the 5-stage in-order CPU using MinorCPU
system.cpu = O3CPU()

# Create a memory bus
system.membus = SystemXBar()
system.system_port = system.membus.cpu_side_ports

# Connect CPU ports to memory bus
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# Interrupt controller (required for full CPU support)
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Set up the program (this should be compiled as a statically-linked binary)
system.workload = SEWorkload.init_compatible('./program')
process = Process()
process.cmd = ['./program']  # Your simple sum loop program
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate the system
root = Root(full_system=False, system=system)
m5.instantiate()

print("Starting simulation...")
exit_event = m5.simulate()

# Print statistics after simulation ends
print(f"Simulation ended at tick {m5.curTick()} because: {exit_event.getCause()}")
