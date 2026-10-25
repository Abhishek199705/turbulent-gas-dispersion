# Import the required modules
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# Cases
cases = {
    "k-epsilon - Molecular": "GasDisp_KE_phi",
    "k-omega_SST - Molecular": "GasDisp_SST_phi",
    "k-epsilon - Turbulence": "GasDisp_KE_turb",
    "k-omega_SST - Turbulence": "GasDisp_SST_turb",
}

# Concentration threshold
T_threshold = 0.3

# Initialize plots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Import the postprocessed data
for case,dir in cases.items():

    probes = Path(dir)/'postProcessing/probes/0/T'
    probes_df = pd.read_csv(probes, sep = r"\s+", names = ["time","source","step","downstream"],skiprows = 5)
    print(probes_df)
    print(probes_df.dtypes)

    # Check the threshold
    for cols in probes_df.columns:
        if cols != "time":
           detected = probes_df[probes_df[cols] >=T_threshold]
           if not detected.empty:
                time = detected["time"].min()
                print(f"The concentration crosses the threshold at the {cols} after {time} s")
           else:
                print(f"The concentration at {cols} does not breach the threshold")



# Plot concentrations

    ax1.plot(probes_df["time"], probes_df["source"], label=case)
    ax2.plot(probes_df["time"], probes_df["step"], label=case)
    ax3.plot(probes_df["time"], probes_df["downstream"], label=case)
ax1.axhline(y=T_threshold, color="red", linestyle="--",label="Detection threshold")
ax2.axhline(y=T_threshold, color="red", linestyle="--",label="Detection threshold")
ax3.axhline(y=T_threshold, color="red", linestyle="--",label="Detection threshold")
ax1.set_title("Concentration profiles close the source of the leak") 
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Tracer (-)")
ax2.set_title("Concentration profiles in the recirculation zone")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Tracer (-)")
ax2.legend()
ax1.legend()
ax3.set_title("Concentration profiles downstream")

ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Tracer (-)")
ax3.legend()
plt.savefig("Concentration vs time")


