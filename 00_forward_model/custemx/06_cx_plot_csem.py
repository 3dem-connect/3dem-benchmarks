#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R / Skibbe.N
"""
# %%
# ########################################################################### #
# # # # #                    Visualization script                     # # # # #
# ########################################################################### #
from custemx.plot import Results
from custemx.plot import plot_line


mod = Results('csem_benchmark_p2_direct')

# %%
ax = plot_line(mod.mp.rx[0], mod.tf[1][0][0, :, 3:], label='tf', figsize=[24, 24])


mod2 = Results('Es_p1_direct')
ax = plot_line(mod2.mp.rx[0], mod2.tf[0][0][0, :, 3:], label='tf', ax=ax)
#ax = plot_line(mod2.mp.rx[0], mod2.pf[0][0, :, :3], label='pf', ax=ax)
#ax = plot_line(mod2.mp.rx[0], mod2.sf[0][0, :, :3], label='sf', ax=ax)
