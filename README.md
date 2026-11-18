# 3dem-benchmarks
Cummunity benchmark examples designed for 3D-EM Connect workshop

## Model description
- **2 layer model**:
    - 1st layer thickness:
        300m
    - resistivities:
        500Ohmm, 5000Ohmm
- **2 possible Tx**:
    - grounded Tx:
        1km from y=-500 to y=500m, x=0, z=0
    - loop Tx:
        1km * 1km - x/y from (-500, -500) to (500, 500) m
- **2 possible rx patches**:
    - central Rx profile:
        4km from x=-2000 to x=2000, y=0, z=0
    - receiver grid:
        4km * 800m with 50m point spacing,
        x/y from (-2000., -400) to (2000, 400) m

- **anomaly geometry**
    - eastern anomaly: thin plate, tilted
        - incl:\
            45°
        - decl:\
            45°
        - thickness:\
            50m
        - size:\
            300m (length) * 500m (width)
        - center position:\
            (500, 0, -150)
        - resistivity:\
            10 Ohmm

    - western anomaly: cylinder
        - size:
            100m radius * 500m length
        - center:
            (400, 100, -150)
        - resistivity:
            5000 Ohmm
        - dip:
            90° (horizontal orientation along x axis)
        - dip_azimuth:
            0°

- **CSEM setup**
    - frequencies:
        [1, 10, 100, 1000, 10000] (Hz)

- **AMT setup**
    - frequencies:
        [1, 10, 100, 1000, 10000] (Hz)
    - no CSEM TX but MT-like sources (d.g., 2 polarizations as boundary-cond.)

- **TEM setup**
    - times:
        [0.0001 - 1] (s), 41 log-steps with 10 per decade between 0.1ms and 1s

## Forward Model
- under custemx
    - Mesh generation: 01_cx_create_benchmark_mesh.py
        - outputs: vtk in meshes/tmp
        - *.1.vtk as 3D mesh
        - *_omega.vtk for anomaly and boundaries only
    - running scripts for csem, amt and tem are provided.
    - central model with layered-earth geometry: 10 * 10 * 10 km
    - outer (halfspace) dimensions: 100 * 100 * 100 km
