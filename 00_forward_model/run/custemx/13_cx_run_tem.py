#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R
"""
# %%
# ########################################################################### #
# # # # #                          example 2                          # # # # #
# ########################################################################### #
# # # # #                      computation script                     # # # # #
# ########################################################################### #

from custemx.mod import Mod

# specify polynomial order and conductivities (air, subsurface)
p = 1     # p = 1 or 2, 3 may be to excessive for this mesh or run very long
sig_vals = {0: 1e-8,
            1: 1/500.,
            2: 1/5000.,
            3: 1/10.,
            4: 1/5000.}

# times 10 log steps per decade

for solver in ['direct']:
    mp = {'name': f'RA_p{p}_{solver}',
          'p': p,
          'sig': sig_vals,
          'approach': 'Et',
          'mode': 'ETD',
          'integrator': 'RA', # IE, RA
          't_min': -4,
          't_max': -0,
          'n_steps': 41}

    mod = Mod(mesh='meshes/benchmark_mesh_csem.xdmf', mp=mp)
    mod.solve(pvd=True)
