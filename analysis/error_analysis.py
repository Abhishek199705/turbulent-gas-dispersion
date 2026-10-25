# Import the necessary modules
import os
from pathlib import Path
import matplotlib.pyplot as plt

# Import the simulation logs
k_epsilon = Path('Airbaseline/log.Airbaseline')
k_omega_SST = Path('Airbaseline_SST/log.Airbaseline_SST')
k_omega_relaxed = Path('Airbaseline_SST_relax/log.relax')

logs = [k_epsilon, k_omega_SST]

fig1,ax1 = plt.subplots(num = "Global Error")
fig2,ax2 = plt.subplots(num = "Sum local error")
for log in logs:
    global_error = []
    sum_local_error = []
    with open (log,"r") as sim:
        lines = sim.readlines()
        for line in lines:
            if line.startswith("time step"):
                step = line
                error = float(line.split()[11].rstrip(","))
                global_error.append(error)
                sum_local = float(line.split()[8].rstrip(","))
                sum_local_error.append(sum_local)
    ax1.plot(global_error)
    ax2.plot(sum_local_error)

fig1.savefig("Global_Continuity_Error.png", dpi=300)
fig2.savefig("Local_Continuity_Error.png", dpi=300)
