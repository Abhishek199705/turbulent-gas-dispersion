# Import the necessary modules
import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Cases
cases = {
    "k-epsilon - Molecular": "GasDisp_KE_phi",
    "k-omega_SST - Molecular": "GasDisp_SST_phi",
    "k-epsilon - Turbulence": "GasDisp_KE_turb",
    "k-omega_SST - Turbulence": "GasDisp_SST_turb",
}

fig,ax = plt.subplots()

for case,dir in cases.items():
    file = Path(dir) /"postProcessing/concentrationLine/0.5/plumeLine_T.xy"
    df = pd.read_csv(file, sep = r"\s+", names = ["x","y","z","T"])
    ax.plot(df["x"],df["T"], label = case)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("T (-)")
ax.set_title("Gas Dispersion Comparison")
ax.legend()
fig.savefig("Dispersion_Comparison.png")
 
