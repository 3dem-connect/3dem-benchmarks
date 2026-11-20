# 3dem-benchmarks
**Cummunity benchmark examples designed for the 3D-EM Connect workshop**

- In this repository, we provide the data required for simulating benchmark
solutions with other software. The repository contains two folders for now:

- Currently, only the owners of this repository are allowed to push into the
*main* branch, for providing updates, please use the *edit* branch or create
additional branches if required

	1) A land-based model to calculate forward responses in form of EM-fields
	or MT-data
	2) A secret model that needs to be recovered by 3D inversing from the
	provided data sets

- Both models are design to work either with a CSEM, AMT, or TEM setup

- Further examples / benchmarks may be added in future

- New simulation results can be sent to us to be uploaded to the repository

- **Consider becoming a developer of this GitHub community repository and
upload new simulation results individually**

## Model descriptions

### 1) Forward model

	Synthetic 2-layer model with 2 anomalies, flat surface.

[Forward model description](./00_forward_model//README.md)

### 2) Secret model

	Synthetic CSEM, AMT (and TEM, work in progress) data are provided to recover
	a synthetic model based on a real-world case study - the final resistivity model of this study
	was smoothed and contrasts enhanced to create a slightly modified subsurface model which allows
	to create high-quality synthetic data sets.

[Secret model description](./01_secret_model//README.md)
