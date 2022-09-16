## Federated Learning Algorithms with Heterogeneous Data Distributions: An Empirical Evaluation

This repository contains TensorFlow codes to simulate different FL algorithms (FedAvg, FedProx, FedDF, FedGKD) 
to tackle non-IID data distributions.

### Data partitioning

The CIFAR10 dataset is partitioned following the paper [Measuring the Effects of Non-Identical Data
Distribution for Federated Visual Classification](https://arxiv.org/abs/1909.06335): a Dirichlet distribution is used to decide the per-client label distribution. 
A concentration parameter controls the identicalness among clients. Very high values for such a concentration parameter, `alpha` in the code, (e.g., > 100.0) imply an identical distribution of labels among clients,
while low (e.g., 1.0) values produce a very different amount of examples for each label in clients, and for very low values (e.g., 0.1) all the client's examples belong to a single class.

### Instructions
`simulation.py` contains the simulations code for FedAvg, FedProx and FedGKD. Hyperparameters can be choosen by manually modifying the
`hp` dictionary. A simulation of each combination of hyperparameters will be run.
Similarly, `simulation_feddf.py` contains the simulations code for FedDF.
Note: before running the simulation(s) the partitioned cifar10 must be created using the provided script (see the following).

#### Creating a virtual environment with venv
`python3 -m venv fd_env`

`source fd_env/bin/activate`

`pip install -r requirements.txt`

The code has been tested with `python==3.8.10`.

#### Creating a virtual environment with venv
Running the simulation(s).

`python3 simulation.py`

`python3 simulation_feddf.py`

#### Creating partitioned CIFAR10   
Before running `simulation.py`, the partitioned CIFAR10 dataset must be generated by executing `dirichlet_partition.py`. 
The script will create a `cifar10_alpha` folder inside the current directory, with three values for alpha (0.1, 1.0, 100.0). This directory will 
contain a folder for each `client` with their examples.

If possible, the `dirichlet_partition.py` will create disjoint dataset for clients.

#### Logging

The `simulation.py` produces logging txt files with per-round metrics. It also creates tensorboard logging files with global model accuracy.

### Datasets
Here a list of datasets used throughout the code.
- [cifar10](https://www.tensorflow.org/datasets/catalog/cifar10).
- [stl10](https://www.tensorflow.org/datasets/catalog/stl10) used only in FedDF.
