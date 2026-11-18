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

# specify frequencies
freqs = [1e0, 1e1, 1e2, 1e3, 1e4]

for solver in ['direct']:
    mp = {'name': f'benchmark_p{p}_{solver}',
          'p': p,
          'frequency': freqs,
          'sig': sig_vals,
          'solver': solver}

    mod = Mod(mesh='meshes/benchmark_mesh.xdmf', mp=mp)
    mod.solve(pvd=True)
