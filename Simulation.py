import numpy as np
import pandas as pd
from scipy.integrate import odeint
import os


# ==========================================
# 1. BIOPHYSICAL & THERMODYNAMIC PARAMETERS
# ==========================================
V_max_base = 5.0    # Maximum astrocytic glutamate clearance rate
K_ATP = 0.5         # ATP affinity for Na+/K+-ATPase pump (mM)
K_m = 1.0           # EAAT transporter affinity for Glutamate
C_basal = 0.2       # Basal ATP consumption for astrocytic survival
k_leak = 0.05       # Passive glutamate diffusion (minimal)
P_basal = 8.0       # Ideal ATP production (full oxygenation condition)


# ==========================================
# 2. SYSTEM DYNAMICS FUNCTIONS (ODEs)
# ==========================================
def P_ATP_dynamic(PaCO2):
    """Calculates ATP production restricted by Vasoconstriction & Bohr Effect"""
    k_v = 0.035
    beta = 0.1
    phi_vaso = np.exp(k_v * (PaCO2 - 40))
    phi_bohr = 1 / (1 + 10**(beta * (40 - PaCO2)))
    return P_basal * phi_vaso * phi_bohr


def bioenergetic_system(state, t, PaCO2, R_stress):
    """Ordinary Differential Equation (ODE) system for the ISB"""
    A, G = state
    A, G = max(1e-5, A), max(1e-5, G) # Prevent mathematical singularity
    
    # Michaelis-Menten kinetics dependent on ATP availability
    V_GLT1 = V_max_base * (A / (K_ATP + A)) * (G / (K_m + G))
    
    # Change in ATP and Glutamate over time (dt)
    dA_dt = P_ATP_dynamic(PaCO2) - C_basal - 4 * V_GLT1
    dG_dt = R_stress - V_GLT1 - k_leak * G
    return [dA_dt, dG_dt]


# ==========================================
# 3. MONTE CARLO ENGINE (N = 2000)
# ==========================================
N_SUBJECTS = 2000
np.random.seed(42) # For reproducibility on Zenodo


# Generate synthetic population with Gaussian Distribution
paco2_pop = np.random.normal(36.0, 4.0, N_SUBJECTS)
r_stress_pop = np.random.normal(1.5, 0.5, N_SUBJECTS)


# Physiological boundaries (Clipping)
paco2_pop = np.clip(paco2_pop, 20.0, 60.0)
r_stress_pop = np.clip(r_stress_pop, 0.5, 4.0)


# Memory allocation for results
final_atp = np.zeros(N_SUBJECTS)
final_glu = np.zeros(N_SUBJECTS)
time_span = np.linspace(0, 100, 500)
state0 = [3.0, 0.2] # Initial homeostasis condition [ATP, Glutamate]


print(f"Running in silico Monte Carlo simulation for {N_SUBJECTS} subjects...")


for i in range(N_SUBJECTS):
    sol = odeint(bioenergetic_system, state0, time_span, args=(paco2_pop[i], r_stress_pop[i]))
    final_atp[i] = sol[-1, 0]
    final_glu[i] = sol[-1, 1]


# ==========================================
# 4. CLINICAL THRESHOLD MAPPING (ISB CLASSIFICATION)
# ==========================================
isb_raw = (3.0 - final_atp) / 3.0 * 5.0
isb_scaled = np.clip(isb_raw, 0.0, 5.0)


df_results = pd.DataFrame({
    'PaCO2_Input': paco2_pop,
    'Amygdala_Stress_Input': r_stress_pop,
    'Final_ATP_Capacity': final_atp,
    'Final_Glutamate_Load': final_glu,
    'ISB_Score': isb_scaled
})


# Ensure data/processed folder exists before saving
os.makedirs('../data/processed', exist_ok=True)
df_results.to_csv('../data/processed/ISB_Monte_Carlo_Results.csv', index=False)
print("Simulation complete. CSV data is ready for publication.")