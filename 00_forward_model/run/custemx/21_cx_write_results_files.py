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
import numpy as np


def write_csem(filename, DATA, frequencies, rx_coords, tx_id=1,
               tx_position=None,
               components=('Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz')):

    nf = len(frequencies)
    nrx = len(rx_coords)

    with open(filename, 'w') as f:
        f.write("# CSEM frequency-domain data\n\n")

        f.write(f"# TX_ID {tx_id:02d}\n\n")
        if tx_position is not None:
            f.write("# TX_POSITION " + " ".join(map(str, tx_position)) + "\n\n")

        f.write(f"# COMPONENTS {' '.join(components)}\n\n")

        f.write(f"# FREQUENCIES_HZ {nf}\n")
        f.write(" ".join(f"{v:.8g}" for v in frequencies) + "\n\n")

        f.write("# RECEIVERS\n# ID X Y Z\n")
        for i, xyz in enumerate(rx_coords):
            f.write(f"{i} " + " ".join(f"{v:.8g}" for v in xyz) + "\n")
        f.write("\n")

        f.write("# CSEM DATA VALUES\n")
        f.write("# COLUMNS Rx_ID " + " ".join(
            f"{c}_{p}" for c in components for p in ('Re', 'Im')
        ))
        f.write("\n")

        for jf in range(nf):
            f.write(f"\n#f{jf:02d}\n")
            for irx in range(nrx):
                row = [str(irx)]
                for z in DATA[jf][irx]:
                    row.extend((f"{z.real:.8e}", f"{z.imag:.8e}"))
                f.write(" ".join(row) + "\n")


def write_amt(filename, DATA, frequencies, rx_coords,
              components=('Zxx', 'Zxy', 'Zyx', 'Zyy', 'Tx', 'Ty')):

    nf = len(frequencies)
    nrx = len(rx_coords)

    with open(filename, 'w') as f:
        f.write("# AMT frequency-domain data\n\n")

        f.write(f"# COMPONENTS {' '.join(components)}\n\n")

        f.write(f"# FREQUENCIES_HZ {nf}\n")
        f.write(" ".join(f"{v:.8g}" for v in frequencies) + "\n\n")

        f.write("# RECEIVERS\n# ID X Y Z\n")
        for i, xyz in enumerate(rx_coords):
            f.write(f"{i} " + " ".join(f"{v:.8g}" for v in xyz) + "\n")
        f.write("\n")

        f.write("# AMT DATA VALUES\n")
        f.write("# COLUMNS Rx_ID " + " ".join(
            f"{c}_{p}" for c in components for p in ('Re', 'Im')
        ))
        f.write("\n")

        for jf in range(nf):
            f.write(f"\n#f{jf:02d}\n")
            for irx in range(nrx):
                row = [str(irx)]
                for z in DATA[jf][irx][:6]:
                    row.extend((f"{z.real:.8e}", f"{z.imag:.8e}"))
                f.write(" ".join(row) + "\n")


def write_tem(filename, DATA, times, rx_coords,
              components=('Ex', 'Ey', 'Ez', 'dBdx', 'dBdy', 'dBdz')):

    nt = len(times)
    nrx = len(rx_coords)

    with open(filename, 'w') as f:
        f.write("# TEM time-domain data\n\n")

        f.write(f"# COMPONENTS {' '.join(components)}\n\n")

        f.write(f"# TIMES_S {nt}\n")
        f.write(" ".join(f"{v:.8g}" for v in times) + "\n\n")

        f.write("# RECEIVERS\n# ID X Y Z\n")
        for i, xyz in enumerate(rx_coords):
            f.write(f"{i} " + " ".join(f"{v:.8g}" for v in xyz) + "\n")
        f.write("\n")

        f.write("# TEM DATA VALUES\n")
        f.write("# COLUMNS Rx_ID " + " ".join(components) + "\n")

        for jt in range(nt):
            f.write(f"\n#t{times[jt]:.8e}\n")
            for irx in range(nrx):
                row = [str(irx)]
                for z in DATA[jt][irx]:
                    row.append(f"{z:.8e}")
                f.write(" ".join(row) + "\n")
# %%  write CSEM E and H-field repsonses

options = ['Et_p2_direct', 'Es_p2_direct']
for option in options:
    mod = Results(option)
    for ipatch in range(mod.mp.nrx):
        for itx in range(mod.mp.ntx):
            patch_data = [mod.tf[jf][ipatch][itx] for jf in range(mod.mp.nf)]
            filename = f"21_11_2026_{option}_Rx{ipatch+1:02d}_Tx{itx+1:02d}.dat"
            write_csem(
                "../../csem_results/custemx/" + filename,
                patch_data,
                mod.mp.frequencies,
                mod.mp.rx[ipatch],
                tx_id=itx+1)


# %%  write AMT Impedance Z and Tipper T responses

options = ['MT_p1_direct', 'MT_p2_direct']
for option in options:
    mod = Results(option)
    for ipatch in range(mod.mp.nrx):
        patch_data = [mod.tf[jf][ipatch] for jf in range(mod.mp.nf)]
        filename = f"R_21_11_2026_{option}_Rx{ipatch+1:02d}.dat"
        write_amt(
            "../../amt_results/custemx/" + filename,
            patch_data,
            mod.mp.frequencies,
            mod.mp.rx[ipatch])


# %%  write AMT Impedance Z and Tipper T responses


mod= Results('Et_p2_direct')
options = ['RA_p1_direct', 'RA_p2_direct']
for option in options:
    for ipat in range(2):
        data = np.load('fwd/' + option + f'/em_data_dbdt_{ipat}.npz')
        for itx in range(2):
            patch_data = data['field_vals'][itx]
            filename = f"21_11_2026_{option}_Rx{ipat+1:02d}_Tx{itx+1:02d}.dat"
            write_tem(
                "../../tem_results/custemx/" + filename,
                patch_data,
                data['time'],
                mod.mp.rx[ipat])

# # # %%
# # ax = plot_line(mod.mp.rx[0], mod.tf[1][0][0, :, 3:], label='tf', figsize=[24, 24])


# # mod2 = Results('Es_p1_direct')
# # ax = plot_line(mod2.mp.rx[0], mod2.tf[0][0][0, :, 3:], label='tf', ax=ax)
# # #ax = plot_line(mod2.mp.rx[0], mod2.pf[0][0, :, :3], label='pf', ax=ax)
# # #ax = plot_line(mod2.mp.rx[0], mod2.sf[0][0, :, :3], label='sf', ax=ax)



# # %%
# options = ['Et_p1_direct', 'Et_p2_iterative', 'Es_p2_iterative',
#            'Es_p2_direct']
# # options = ['Es_p1_direct', 'Et_p1_direct', 'Et_p2_direct', 'Et_p1_iterative',
# #            'Et_p2_iterative']
# #options = ['Es_p1_direct', 'Et_p1_direct', 'Et_p2_direct', 'Et_p1_iterative']

# options = ['Et_p1_direct', 'Es_p1_direct', #'Et_p2_direct', 'Es_p1_direct', 'Es_p2_direct',
#            'Et_p1_iterative', 'Es_p1_iterative']
# nf = 0
# ri= 0
# ti = 0
# mod = Results(options[0])
# ax = plot_line(mod.mp.rx[ri], mod.tf[nf][ri][ti, :, 3:],
#                label=options[0], figsize=[24, 24])

# for option in options[1:]:
#     mod = Results(option)
#     ax = plot_line(mod.mp.rx[ri], mod.tf[nf][ri][ti, :, 3:],
#                    label=option, ax=ax, markersize=2)
