# Secret Model description

## Notes to consider before inversion

- The full synthetic data sets are comparatively dense and do not represent a
  realistic land-based EM survey coverage.

- We provide such large data sets since it is possible (and recommended,
  depenending on inversion codes and computational resources), to reduce the
  amount of data individually by deselecting noisy data, certain frequencies,
  transmitters, keep only every N-th receiver, or do not use all components.

- This specific secret model was chosen because topographic variations in
  the survey area are present, but not significant. Inversion runs may neglect
  topography data if this substantially simplifies the computational setup.

- The underlying resistivity distribution is not disclosed. Resistivity values
  in the subsurface model are within the common limits of real-world cases.

## Survey Geometry

The secret model is based on the inversion results of a real survey and covers
an area of 4 x 4 km, which was translated to a synthetic origin.
Correspondingly, the measured field data of all EM data types cover a 4 x 4 km
area and the provided topography data fit to the synthetic origin.

- Origin of local coordinate system:
    * lat, lon = [3°, 3°]
    * easting, northin = [500000.0, 331593.1795450], UTM zone 31N

- Topography data are provided as ESRI ASCII grid and xyz file in the
  *data/topo.zip* directory

## Data description

**1) AMT data**

- The provided dataset consists of impedance tensor and tipper measurements at

- 41 * 41 (1681) station receiver grid in a 4 x 4 km area, 100 m stn spacing

- range of receiver stations: -2000 - 2000 m in x and y directions

- Error model: Derived from variances of a real AMT data set, by using the
  median standard variation per Z or T comonent and frequency to generate a
  new error vector with random noise, with an additional small bias.

**2) CSEM data**

- added very soon

**3) TEM data**

- added soon