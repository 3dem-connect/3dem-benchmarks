#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R / Skibbe.N
"""
# %%
# ########################################################################### #
# # # # #                    Visualization script                     # # # # #
# ########################################################################### #

import numpy as np
from custemx.plot import Results
from custemx.plot import plot_line

import sys
sys.path.insert(0, '../../utils')
from writers_responses import write_amt, write_csem, write_tem


# %%  write CSEM E and H-field repsonses

# options = ['Et_p2_direct', 'Es_p2_direct']
# for option in options:
#     mod = Results(option)
#     for ipatch in range(mod.mp.nrx):
#         for itx in range(mod.mp.ntx):
#             patch_data = [mod.tf[jf][ipatch][itx] for jf in range(mod.mp.nf)]
#             filename = f"21_11_2026_{option}_Rx{ipatch+1:02d}_Tx{itx+1:02d}.dat"
#             write_csem(
#                 "../../csem_results/custemx/" + filename,
#                 patch_data,
#                 mod.mp.frequencies,
#                 mod.mp.rx[ipatch],
#                 tx_id=itx+1)


# # %%  write AMT Impedance Z and Tipper T responses

# options = ['MT_p1_direct', 'MT_p2_direct']
# for option in options:
#     mod = Results(option)
#     for ipatch in range(mod.mp.nrx):
#         patch_data = [mod.tf[jf][ipatch] for jf in range(mod.mp.nf)]
#         filename = f"21_11_2026_{option}_Rx{ipatch+1:02d}.dat"
#         write_amt(
#             "../../amt_results/custemx/" + filename,
#             patch_data,
#             mod.mp.frequencies,
#             mod.mp.rx[ipatch])


# %%  write AMT Impedance Z and Tipper T responses


mod= Results('Et_p2_direct')
options = ['RA_p1_direct', 'RA_p2_direct']

for option in options:
    for ipat in range(2):
        datae = np.load('fwd/' + option + f'/em_data_e_{ipat}.npz')
        datam = np.load('fwd/' + option + f'/em_data_dbdt_{ipat}.npz')
        data = np.concatenate((datae['field_vals'], datam['field_vals']), 
                              axis=-1)
        for itx in range(2):
            patch_data = data[itx]
            filename = f"21_11_2026_{option}_Rx{ipat+1:02d}_Tx{itx+1:02d}.dat"
            write_tem(
                "../../tem_results/custemx/" + filename,
                patch_data,
                datae['time'],
                mod.mp.rx[ipat])


# # # %%
# # ax = plot_line(mod.mp.rx[0], mod.tf[1][0][0, :, 3:], label='tf', figsize=[24, 24])


# # mod2 = Results('Es_p1_direct')
# # ax = plot_line(mod2.mp.rx[0], mod2.tf[0][0][0, :, 3:], label='tf', ax=ax)
# # #ax = plot_line(mod2.mp.rx[0], mod2.pf[0][0, :, :3], label='pf', ax=ax)
# # #ax = plot_line(mod2.mp.rx[0], mod2.sf[0][0, :, :3], label='sf', ax=ax)


# %%
# options = ['Et_p1_direct', 'Et_p2_iterative', 'Es_p2_iterative',
#            'Es_p2_direct']
# options = ['Es_p1_direct', 'Et_p1_direct', 'Et_p2_direct', 'Et_p1_iterative',
#            'Et_p2_iterative']
options = ['Es_p2_iterative', 'Et_p1_direct', 'Et_p2_direct']

# options = ['Et_p1_direct', 'Es_p1_direct', #'Et_p2_direct', 'Es_p1_direct', 'Es_p2_direct',
#            'Et_p1_iterative', 'Es_p1_iterative']
nf = 1
ri= 0
ti = 0
mod = Results(options[0])
ax = plot_line(mod.mp.rx[ri], mod.tf[nf][ri][ti, :, :3],
               label=options[0], figsize=[24, 24])
# ax = plot_line(mod.mp.rx[ri], mod.pf[nf][ri][ti, :, 3:],
#                label='pf', ax=ax)
# ax = plot_line(mod.mp.rx[ri], mod.sf[nf][ri][ti, :, 3:],
#                label='sf', ax=ax)


for option in options[1:]:
    mod = Results(option)
    ax = plot_line(mod.mp.rx[ri], mod.tf[nf][ri][ti, :, :3],
                   label=option, ax=ax, markersize=2)
