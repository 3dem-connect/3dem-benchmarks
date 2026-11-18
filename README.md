# 3dem-benchmarks
Cummunity benchmark examples designed for the 3D-EM Connect workshop

In this repository, we provide the data required for simulating benchmark solutions with other software.
The repository contains two folders for now:

	1) A model to calculate forward responses in form of EM-fields or MT-data
	2) A secret model that needs to re recovered by 3D inversing from the provided data sets

Both models are design to work either with a CSEM, AMT, or TEM setup

The repository may be extended with furhter benchmark examples in the future and community members
willing to contribute are welcome to add their simulation results for others with a short description

## Model descriptions

	**1) Forward model**

		Synthetic 2-layer model with 2 anomalies, flat surface.

		[Forward model description](./00_forward_model//README.md)

	**2) Secret model**

		Synthetic CSEM, AMT (and TEM, work in progress) data are provided to recover
		a synthetic model based on a real-world case study - the final resistivity model of this study
		was smoothed and contrasts enhanced to create a slightly modified subsurface model which allows
		to create high-quality synthetic data sets.

		[Secret model description](./00_secret_model//README.md)
