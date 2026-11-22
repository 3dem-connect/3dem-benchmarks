# 3dem-benchmarks

## Cummunity benchmark examples designed for the 3D-EM Connect workshop

- This repository provides the data required for simulating benchmark
  solutions with different software. The repository contains two examples for
  now

- **Forward benchmark:** A land-based model to calculate forward responses in
  form of EM-fields or MT-data

- **Secret model:** A secret model containng strucutres down to 1km depth to
  be recovered by 3D inversing

- Both examples are designed to work for AMT, CSEM, and TEM setups

- Further examples / benchmarks may be added in future

## Please read before starting

- **Consider becoming a developer of this GitHub community repository for
  contribtuing and uploading new simulation results individually**

- Report bugs or ask questions by opening issues in the repository or reaching
  out to the workshop organizers

- Simulation results can be also sent to the workshop organizers

- Consider using our perferred data formats or suggest alternatives

- Currently, only the owners of this repository are allowed to push into the
  *main* branch, for providing updates, please use the *edit* branch or create
  additional branches if required

- This is just the beginning of a community-driven repository. Its future
  direction and development will depend on the interest, feedback, and
  engagement of the community.

## Model descriptions

### 1) Forward model

	Synthetic 2-layer model with 2 anomalies, flat surface.

[Forward model description](./00_forward_model//README.md)

### 2) Secret model

	Synthetic CSEM, AMT (and TEM, work in progress) data are provided to
	recover a synthetic model based on a real-world case study - the final
	resistivity model of this study was smoothed at the surface and contrasts
	at greater depths slightly enhanced to create the synthetic data sets.

[Secret model description](./01_secret_model//README.md)
