# AiiDA-FANS

[![PyPI Package][pypi-badge]][pypi-link]
[![Docs Status][docs-badge]][docs-link]
[![Build Status][ci-badge]][ci-link]

> [!WARNING]  
> Critical content demanding immediate user attention due to potential risks.

This is a plugin for [AiiDA][aiida-link] that facilitates the use of [FANS][FANS-link]. FANS is an FFT-based homogenisation solver for microscale and multiphysics problems. It is an open-source project under active development at the Institute of Applied Mechanics, University of Stuttgart. This plugin aims to bring the full value of provenance tracking and database integration to the results produced by FANS.

The design goals of this plugin are to provide a simple but powerful user interface to FANS. In doing so, the plugin packages additional utilities to eliviate some of the burdens we perceive in the traditional AiiDA workflow.


## Installation

AiiDA-FANS is available on the PyPI and conda-forge channels. Our recommended method of installing AiiDA-FANS is to use the pixi package manager, in which case `pixi add aiida-fans` will install the plugin from conda-forge by default, as well as its dependencies: python, AiiDA, and h5py. 

Otherwise, the package can be installed with pip by `pip install aiida-fans` or with mamba by `mamba install aiida-fans`.

In any case, the user is responsible for installing FANS and ensuring it is accessible to the plugin. This can be achieved without need for further customisation by having FANS accessible on the PATH environment variable. Please consult the [FANS repository][FANS-link] for more information on the installation of this software.


## Usage

To use this plugin, you must first establish an AiiDA profile, computer, and code. For help on how to do this please refer to the [AiiDA installation][AiiDA-install-link] guide.

For general information on the usage of AiiDA you should refer to the [AiiDA documentation][AiiDA-docs-link], and for the usage of FANS refer to its [repository][FANS-link].

This plugin offers some utilities to help smooth the AiiDA user experience. Namely, the `utils.run_fans` function which allows you to provide the inputs for a job as a dictionary of mostly pythonic values. This utility will parse these inputs and automatically use any appropriate existing nodes it finds in your profile before making new nodes where necessary. For more information on this plugin's specifics and how to use the utilities, please refer to the [documentation][docs-link].

## Tutorial

A tutorial accompanies this plugin. To try it out: clone this repository, cd into it, run `pixi install -e tutorial` and `marimo run tutorial/tutorial.py`. For more information before you begin, take a look at `./tutorial/README.md`.

## Contact

You can contact ethan.shanahan@gmail.com with any questions regarding the AiiDA-FANS plugin and accompanying tutorial.

<!-- URLs -->
[pypi-badge]: https://badge.fury.io/py/aiida-fans.svg
[pypi-link]: https://badge.fury.io/py/aiida-fans
[ci-badge]: https://github.com/ethan-shanahan/aiida-fans/actions/workflows/ci.yml/badge.svg?branch=main
[ci-link]: https://github.com/ethan-shanahan/aiida-fans/actions
[docs-badge]: https://readthedocs.org/projects/aiida-fans/badge
[docs-link]: http://aiida-fans.readthedocs.io/
[AiiDA-docs-link]: https://aiida-core.readthedocs.io/
[AiiDA-install-link]: https://aiida.readthedocs.io/projects/aiida-core/en/latest/installation/index.html
[FANS-link]: https://github.com/DataAnalyticsEngineering/FANS
