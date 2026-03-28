# Bioenergetic Stability Index (ISB): Computational Modeling & Causal Analysis

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19269341.svg)](https://doi.org/10.5281/zenodo.19269341)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview
This repository contains the computational pipeline, mathematical modeling scripts, and summary statistics guidelines for the manuscript: **"Mechanistic Reconstruction of Integrative Psychopathology: A Theoretical Framework, Computational Modeling of the Bioenergetic Stability Index (ISB), and Mendelian Randomization Causal Analysis"**.

The project proposes the **Bioenergetic Stability Index (ISB)**, a mathematical algorithm that reconstructs anxiety disorders and Major Depressive Disorder (MDD) as emergent manifestations of systemic bioenergetic failure, primarily triggered by peripheral allostatic load such as Gastroesophageal Reflux Disease (GERD).

This repository provides:
1. The **Non-linear Ordinary Differential Equation (ODE)** framework simulating astrocytic ATP depletion and synaptic glutamate accumulation.
2. The **Monte Carlo perturbation simulation** pipeline for an *in silico* population ($N=2000$).
3. Guidelines for the **Bidirectional Mendelian Randomization (MR)** analysis utilizing summary-level GWAS data.

## Repository Structure
```text
data/
  raw/                  # (Placeholder) GWAS summary statistics links
  processed/            # Synthesized Monte Carlo population data outputs
notebooks/
  01_isb_ode_simulation.ipynb   # ODE stability analysis and Phase Portraits
  02_monte_carlo_population.ipynb # Probabilistic simulation for N=2000
src/
  __init__.py
  thermodynamics.py     # Core Michaelis-Menten & bioenergetic functions
  simulation.py         # Monte Carlo execution engine
  mr_analysis.R         # TwoSampleMR pipeline for causal inference
results/
  figures/              # Trajectory plots, ROC curves, and MR scatter plots
requirements.txt        # Python dependencies
LICENSE
README.md
Mathematical Architecture: Thermodynamic ODEs
​The core of the ISB computational model evaluates the trajectory of astrocytic ATP (A) and extracellular glutamate (G) over time. The system's equilibrium is dictated by the efficiency of the Na+/K+-ATPase pump and the EAAT2/GLT-1 transporter under varying levels of oxygen delivery (modulated by PaCO2 and the Bohr effect).
​The core dynamic system is defined as:
$$ \frac{dA}{dt} = P_{ATP}(PaCO_2) - C_{basal} - 4 \cdot V(A, G) $$
$$ \frac{dG}{dt} = R_{stress} - V(A, G) - k_{leak} \cdot G $$
​Where the transporter kinetics strictly rely on remaining ATP reserves:
$$ V(A,G) = V_{max_base} \cdot \frac{A}{K_{ATP} + A} \cdot \frac{G}{K_m + G} $$
​For full derivations and Jacobian matrix stability criteria, please refer to the primary manuscript.
​Installation & Requirements
​To run the simulations locally, clone this repository and install the required dependencies:git clone [https://github.com/cefiyana-clover/ISB-Computational-Psychiatry.git](https://github.com/cefiyana-clover/ISB-Computational-Psychiatry.git)
cd ISB-Computational-Psychiatry
pip install -r requirements.txt
Core Dependencies:
​numpy
​pandas
​scipy (for ODE integration via odeint)
​matplotlib & seaborn (for phase plane visualization)
​TwoSampleMR (R package for Mendelian Randomization)
​Usage
​1. Running the Bioenergetic ODE Simulation:
Navigate to the src/ directory and execute the primary simulation script to generate the bioenergetic trajectories:python src/simulation.py
This will output the ISB_Monte_Carlo_Results.csv file into the data/processed/ directory.
​2. Mendelian Randomization Analysis:
The MR scripts are written in R. Ensure you have the TwoSampleMR package installed. Execution requires downloading the public GWAS summary statistics (see Data Availability).
​Data Availability
​No new individual-level human data were collected. The Mendelian Randomization scripts utilize publicly available Genome-Wide Association Studies (GWAS) summary statistics:
​GERD Exposure: An et al. (2019) via GWAS Catalog (GCST90000514).
​MDD Exposure: Wray et al. (2018) via Psychiatric Genomics Consortium (PGC) or GWAS Catalog (GCST005839).
​Citation
​If you utilize this code, the ODE framework, or the theoretical concepts presented in this repository, please cite the associated preprint/manuscript:
​Cefiyana. (2026). Mechanistic Reconstruction of Integrative Psychopathology: A Theoretical Framework, Computational Modeling of the Bioenergetic Stability Index (ISB), and Mendelian Randomization Causal Analysis. Zenodo. DOI: https://doi.org/10.5281/zenodo.19269341
​License
​This project is licensed under the MIT License - see the LICENSE file for details.
