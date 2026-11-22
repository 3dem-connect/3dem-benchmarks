#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R / Skibbe.N
"""
# %%
# ########################################################################### #
# # # # #        Forward modeling benchmark simulation script         # # # # #
# ########################################################################### #
from custemx.mod import Mod

# Notice: p = 1 or 2, 3 can be tested but is likely too excessive for
# the chosen refinement of the model setup

sig_vals = {0: 1e-8,
            1: 1/500.,
            2: 1/5000.,
            3: 1/10.,
            4: 1/5000.}

# specify frequencies
freqs = [1e0, 1e1, 1e2, 1e3, 1e4]

# for p in [1, 2]:
#     for solver in ['direct', 'iterative']:
#         mp = {'name': f'Et_p{p}_{solver}',
#               'p': p,
#               'frequency': freqs,
#               'sig': sig_vals,
#               'solver': solver}

#         mod = Mod(mesh='meshes/benchmark_mesh_csem.xdmf', mp=mp)
#         mod.solve(pvd=True)   # pvd=True to export results on global mesh for Paraview

# %% run with secondary field approach alternatively

sig_0 = {0: 1e-8,
         1: 1/500.,
         2: 1/5000.,
         3: 1/500.,
         4: 1/500.}

for p in [1, 2]:
    for solver in ['direct', 'iterative']:
        mp = {'name': f'Es_p{p}_{solver}',
              'p': p,
              'approach': 'Es',
              'frequency': freqs,
              'sig': sig_vals,
              'sig_0': sig_0,
              'sig_layered': [1/500., 1/5000.],
              'layer_thick': [300.],
              'max_dipole_length': 20.,
              'procs_per_proc': 10,
              'solver': solver}

        mod = Mod(mesh='meshes/benchmark_mesh_csem.xdmf', mp=mp)
        mod.solve(pvd=True)   # pvd=True to export results on global mesh for Paraview
