# 3dem-benchmarks
Cummunity benchmark examples designed for 3D-EM Connect workshop

## Forward Model
- under custemx
    - Mesh generation: 01_cx_create_benchmark_mesh.py
        - outputs: vtk in meshes/tmp
        - *.1.vtk as 3D mesh
        - *_omega.vtk for anomaly and boundaries only
    - running scripts for csem, amt and tem are provided.

### Model description
- 2 layer model, thickness: 300, values: 500, 5000 Ohmm
- 2 tx
    - grounded tx line 1 km y directed, x=0 (10m segments)
    - tx loop, 1km * 1km, (-500, -500) to (500, 500) (10m segments)

- 2 rx grids, and two lines
    - each side lines in x: 2km to each side (20m segments)
    - receiver grid: 4km * 800m, (50m spacing)
    - z = -0.1 (in the ground, z positive upwards)

- anomaly geometry
    - eastern anomaly: thick plate, tilted
        - incl:45°
        - decl:45°
        - thickness: 50m
        - size: x:300m * y:500m
        - position: (500, 0, -150)
        - resistivity: 10 Ohmm

    - western anomaly: zylinder
        - size: 100m * 500m
        - center: (400, 100, -150)
        - resistivity: 5000 Ohmm
        - dip: 90
        - dip_azimuth: 0

- frequencies: [1, 10, 100, 1000, 10000] (Hz)
- outer geometry: (-40000, -40000, -40000) to (40000, 40000, 40000)
