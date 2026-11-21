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

# move Rx a bit into the subsurface, 10 cm
rx1[:, 2] = -0.1
rx2[:, 2] = -0.1

# %% create mesh for amt setup without Tx

allrx = np.unique(np.vstack((rx1, rx2)), axis=0)
rx_tri = mu.refine_rx(allrx, r=5.)

dim = 5e3
M = BlankWorld(x_dim=[-dim, dim],
               y_dim=[-dim, dim],
               z_dim=[-dim, dim],
               name='benchmark_mesh_amt',
               preserve_edges=True)

# add transmitter: crooked loop transmitter, defined in *synthetic_definitions*
M.build_surface(insert_paths=rx_tri)

# build layered earth mesh and extend 2D surface mesh to 3D world
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