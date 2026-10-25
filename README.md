# Turbulent Gas Dispersion and Virtual Gas Detection Using OpenFOAM

**Computational Fluid Dynamics | OpenFOAM 6 | RANS Turbulence | C++ | Python**

## Project Overview

This project investigates the dispersion of a passive gaseous tracer in turbulent airflow over a backward-facing step using OpenFOAM Foundation 6.

The main objective is to understand how turbulence modelling and turbulent scalar diffusion influence gas concentration distributions, flow recirculation, and virtual gas-detector response.

Two Reynolds-Averaged Navier–Stokes (RANS) turbulence models are investigated:

- Standard k-ε
- k-ω Shear Stress Transport (SST)

A custom solver, `scalarTransportTurbFoam`, was developed by modifying OpenFOAM's `scalarTransportFoam` to account for turbulent scalar diffusivity.

The project demonstrates a CFD workflow combining numerical simulation, solver development, and Python-based engineering analysis.

## 1. Objectives

- Simulate steady turbulent airflow over a backward-facing step.
- Compare k-ε and k-ω SST turbulence predictions.
- Investigate numerical convergence, continuity errors and flow reattachment.
- Implement turbulent scalar diffusivity in a custom OpenFOAM solver.
- Compare molecular-only and turbulence-enhanced tracer transport.
- Evaluate transient tracer concentration at three virtual detector locations.

## 2. Numerical Methodology

### 2.1 Airflow Simulation

Steady-state incompressible airflow is simulated using `simpleFoam`.

The geometry is based on the OpenFOAM `pitzDaily` backward-facing-step case, with an inlet velocity of approximately 10 m/s.

Two turbulence models are compared: standard k-ε and k-ω SST.

Solver residuals and continuity errors are examined to assess numerical convergence. The flow-separation region is studied using near-wall velocity profiles.

### 2.2 Scalar Transport

After solving the airflow, the converged velocity and face-flux fields are transferred to transient scalar-transport simulations.

The passive scalar transport equation is:

\[
\frac{\partial T}{\partial t}
+\nabla\cdot(\mathbf{U}T)
=
\nabla\cdot(D_{\mathrm{eff}}\nabla T)
\]

where:

- \(T\): normalized tracer concentration
- \(\mathbf U\): prescribed velocity field
- \(D_{\mathrm{eff}}\): effective scalar diffusivity

For molecular-only dispersion:

\[
D_{\mathrm{eff}}=D_m
\]

For turbulence-enhanced dispersion:

\[
D_{\mathrm{eff}}=D_m+\frac{\nu_t}{Sc_t}
\]

The molecular diffusivity is set to \(1.6\times10^{-5}\,\mathrm{m^2/s}\), and the turbulent Schmidt number is set to 0.7.

The scalar transport simulation is transient, while the airflow remains fixed. Consequently, the model uses one-way coupling.

### 2.3 Custom OpenFOAM Solver

The custom solver `scalarTransportTurbFoam` was developed from OpenFOAM Foundation 6's `scalarTransportFoam`.

The original molecular diffusion term:

```cpp
- fvm::laplacian(DT, T)
```

was replaced with:

```cpp
- fvm::laplacian(Deff, T)
```

where the effective diffusivity includes the turbulent viscosity obtained from the converged RANS simulation.

The implementation enables comparison of molecular-only transport and turbulence-enhanced tracer mixing.

The pressure-corrected face flux `phi` from `simpleFoam` is retained for the scalar calculations. An upwind convection scheme was used to obtain bounded tracer solutions in the investigated cases.

## 3. Simulation Cases

Four modelling configurations were investigated.

| Case | Turbulence model | Scalar diffusion |
|---|---|---|
| `GasDisp_KE_phi` | k-ε | Molecular only |
| `GasDisp_SST_phi` | k-ω SST | Molecular only |
| `GasDisp_KE_turb` | k-ε | Molecular + turbulent |
| `GasDisp_SST_turb` | k-ω SST | Molecular + turbulent |

These simulations allow the influence of turbulence-model selection and turbulent scalar diffusivity to be studied separately.

## 4. Results and Discussion

### 4.1 Solver Convergence

Both airflow simulations reached their configured convergence criteria.

The SST model initially experienced convergence difficulties. Adjusting the solver relaxation factors improved numerical stability.

Residual and continuity-error histories were analysed using Python.



### 4.2 Flow Separation and Reattachment

The backward-facing step produces a recirculation region with reversed near-wall flow.

Approximate reattachment locations were identified from near-wall streamwise velocity sign changes.

| Turbulence model | Approximate reattachment location |
|---|---|
| k-ε | 0.1654 m |
| k-ω SST | 0.1873 m |

The SST simulation predicts a reattachment location approximately 13.2% farther downstream than k-ε.

These values are estimates based on near-wall velocity sampling rather than a wall-shear-stress calculation.

### 4.3 Effect of Turbulent Diffusion

The molecular-only cases exhibit pronounced variations in tracer concentration along the selected horizontal sampling line.

Including turbulent diffusivity produces smoother concentration distributions and changes the predicted transport into the separated-flow region.



The results demonstrate that modelling turbulent scalar transport can significantly influence predicted concentrations.

### 4.4 Virtual Gas-Detector Analysis

Three virtual detector positions were defined using OpenFOAM's `probes` function object.

| Detector | Position (m) | Location |
|---|---|---|
| D1 | (-0.015, 0.002, 0) | Near source |
| D2 | (0.010, -0.005, 0) | Recirculation region |
| D3 | (0.100, 0.008, 0) | Downstream |

Transient concentration histories were extracted from all four simulations.

An illustrative normalized concentration threshold of 0.3 was used to investigate detector response.


**Key observations:**

- D1 detects the tracer early in all four simulations.
- Turbulent-diffusion cases predict earlier threshold crossings at D2.
- D3 remains below the illustrative detection threshold in all four cases.
- Including turbulent diffusion increases the predicted tracer signal at D3.

The study highlights the sensitivity of predicted detector response to both location and scalar-transport modelling assumptions.

## 5. Numerical and Physical Limitations

The project is a CFD learning and engineering case study, not a validated industrial gas-release simulation.

Current limitations include:

- One-way coupling between airflow and tracer transport.
- Constant-density airflow without composition-dependent buoyancy.
- No chemical reactions or energy coupling.
- Steady RANS airflow rather than resolved transient turbulence.
- Near-wall mesh resolution requiring further assessment.
- No completed mesh-independence or experimental-validation study.


Tracer concentration is normalized and must not be interpreted as a calibrated gas concentration or industrial alarm measurement.

## 6. Future Work

Potential extensions include:

1. Mesh-refinement and validation studies.
2. Sensitivity analysis of the turbulent Schmidt number.
3. Nonreactive air–CO₂ species transport.
4. Two-way coupling between species, density, momentum and buoyancy.
5. Realistic gas-release boundary conditions.
6. Industrial geometry and ventilation modelling.
7. Improved gas-detector placement studies.

## 7. Software and Tools

| Tool | Application |
|---|---|
| OpenFOAM Foundation 6 | CFD simulations |
| C++ | Custom scalar-transport solver |
| ParaView | Flow and tracer visualization |
| Python | Post-processing |
| Pandas | Numerical data handling |
| Matplotlib | Engineering plots |


## 8. Conclusions

This project demonstrates a CFD workflow involving turbulent airflow modelling, transient scalar transport, custom solver modification and virtual detector analysis.

The principal result is that including turbulent scalar diffusion substantially influences the predicted tracer distribution and detector response in separated turbulent flow.

The work also demonstrates the importance of numerical consistency, turbulence-model selection and a clear understanding of simulation limitations when applying CFD to gas-dispersion problems.

---

**Project focus:** Turbulent flow, scalar transport and CFD-based gas-detection analysis.

**Status:** Initial CFD study completed; coupled dense-gas modelling identified as future work.
