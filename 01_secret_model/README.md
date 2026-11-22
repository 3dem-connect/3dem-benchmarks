# Secret Model description

## Read before running inversion

- All synthetic data are provided as full data sets (including also data below
  the noise level) for 451 RX stations for each method.

- Topographic variations in the survey area are present, but smooth and
  within maximum 100 m difference over the complete modeling domain. Inversion
  runs may neglect topography data if this substantially simplifies the
  computational setup. In this case, modify Rx height to zero or below surface.

- The elevation of the receiver stations is alaways positive and corresponds to
  the height of the stations based on the digital elevation model (DEM) -1 m in
  the model domain used for creating the synthetic data. Depending on cell
  sizes and interpolation procedures for DEM data in different codes,
  the provided z-coordinates of RX stations may not be within the subsurface
  and may be shifted downwards for all or single stations.

- Noisy data should be masked individually by using the provided error data,
  which are consistent with the errors models applied to the synthetic data.

- Depenending on different inversion codes and available computational
  resources, it is absolutely possible to keep only every N-th receiver,
  do not use all components, ...

- The underlying resistivity distribution is not disclosed. Resistivity values
  in the subsurface model are within the common limits of real-world cases and
  all features of the secret model are within 1 km depth from the surface.

## Survey Geometry

- The secret model is based on inversion results of a real EM case study and
  covers an area of 4 x 4 km, which was translated to a synthetic coordinate
  origin. Correspondingly, the measured field data of all EM data types cover
  a 4 x 4 km area and the provided topography data fit to the synthetic origin.

- Origin of local coordinate system:
    * lat, lon = [3°, 3°]
    * easting, northing = [500000.0, 331593.1795450], UTM zone 31N

- Topography data are provided as ESRI ASCII grid and xyz file in the
  *data/topo.zip* directory

## Data description

**1) AMT data**

- Impedance and tipper data are provided as edi-files: *data/noisy.zip*

- Error model: corresponds to the provided variances in the edi files

- Other common error models may be applied as well

- If of interest, the noisefree data are uploaded as well: *data/noisefree.zip*

- The data follow common MT convention as provided, e.g., in the [MT3DINV4 edi
  workshop files](https://mt3dinv4.mtnet.info/Secret_model.html)

- Impedance data in the edi files are in (mV/km/nT), and all data are stored
  using the common North-East-Downward (NED) convention of the MT community

- The provided dataset consists of impedance tensor and tipper measurements at

- 11 * 41 (451) station receiver grid in a 4 x 4 km area with
  400 m line and 100 m stations spacing

- range of receiver stations: -2000 - 2000 m in x and y directions

- coordinates of topo files follow common UTM easting & northing convention

**2) CSEM data**

- added soon

**3) TEM data**

- added soon