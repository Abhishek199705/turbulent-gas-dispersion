# Import the required modules
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
# Import the required files
k_epsilon = Path("Airbaseline/postProcessing/reattachmentLine/295/nearWall_U.xy")
k_omega_SST = Path("Airbaseline_SST_relax/postProcessing/reattachmentLine/2143/nearWall_U.xy")

cases = [k_epsilon,k_omega_SST]

# Find the reattachment length
fig,ax = plt.subplots()

for case in cases:
    df = pd.read_csv(case,sep = r"\s+",names=['x','y','z','Ux','Uy','Uz'])
    ax.plot(df["x"],df["Ux"], label= case.parents[3].name)
    ax.legend()
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Ux (m/s)")
    ax.axhline(y=0, color="black", linestyle="--")
    ax.set_title("Near wall velocity")
    #print(df)
    for id,row in df.iterrows():
        if id !=0:
            if row["Ux"] >0 and df.iloc[id-1]["Ux"] < 0:
               reattach_length = row["x"]
    print(f"Reattachment for {case} is at {reattach_length} m")
    plt.savefig("Reattachment_comparison.png")


