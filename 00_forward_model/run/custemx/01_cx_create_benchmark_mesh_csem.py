# -*- coding: utf-8 -*-
"""
@author: Rochlitz.R
"""

# ########################################################################### #
# # # # #                          example 2                          # # # # #
# ########################################################################### #
# # # # #                    mesh generation script                   # # # # #
# ########################################################################### #

from email import header
from custemx.meshtools.meshgen_tools import BlankWorld
from custemx.meshtools import meshgen_utils as mu
import numpy as np


rx1 = mu.line_x(start=-1.5e3, stop=1.5e3, n_segs=150, z=0.)
rx2 = mu.rx_grid([-1.5e3, 1.5e3, 61], [-4e2, 4e2, 9], z=0.)

tx1 = mu.line_y(start=-500., stop=500., n_segs=100)
tx2 = mu.loop_r(start=[-500., -500.], stop=[500., 500.], n_segs=400)

# save survey geometry to use with other simulation software
np.savetxt('../setup/rx_line.dat', rx1,
           header='Rx Pos: x, y, z (m)', fmt='%.3f')
np.savetxt('../setup/rx_grid.dat', rx2,
           header='Rx Pos: x, y, z (m)', fmt='%.3f')

np.savetxt('../setup/tx_grounded.dat', tx1,
           header='Rx Pos: x, y, z (m)', fmt='%.3f')
np.savetxt('../setup/tx_loop.dat', tx2,
           header='Rx Pos: x, y, z (m)', fmt='%.3f')

# move Rx a bit into the subsurface, 10 cm
rx1[:, 2] = -0.1
rx2[:, 2] = -0.1

allrx = np.unique(np.vstack((rx1, rx2)), axis=0)

# remove rx refinement triangles at intersections with Tx wires
x_remove = [-500., 0., 500.]
allrx = allrx[~np.any(np.isclose(allrx[:, 0, None], x_remove), axis=1)]
rx_tri = mu.refine_rx(allrx, r=5.)

# %% create mesh with Tx for CSEM / TEM
dim = 5e3
M = BlankWorld(x_dim=[-dim, dim],
               y_dim=[-dim, dim],
               z_dim=[-dim, dim],
               name='benchmark_mesh_csem',
               preserve_edges=True)

# add transmitter: crooked loop transmitter, defined in *synthetic_definitions*
M.build_surface(insert_tx=[tx1, tx2], insert_paths=rx_tri)

# build layered earth mesh and extend 2D surface mesh to 3D world
#M.build_halfspace_mesh()
M.build_layered_earth_mesh(layer_depths=[-300.])   #500, 5000 Ohm
M.add_rx(rx1)
M.add_rx(rx2)

# plate / brick resisitivity: 10, 50
M.add_plate(300., 500., 50., [-500., 0., -150.], 45., 45., cell_size=1e3)
M.add_cylinder(100., 500., origin=[400., 100., -150.], n_segs=32,
               dip=90., dip_azimuth=0., cell_size=1e4)

# extend the computational domain (reduce boundary artifacts for low freqs.)
M.extend_world(x_fact=10., y_fact=10., z_fact=10.)

# call TetGen
M.call_tetgen(tet_param='-pq1.3aAD')