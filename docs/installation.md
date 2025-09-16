# Installation

AiiDA-FANS is available on the PyPI and conda-forge channels. Our recommended method of installing AiiDA-FANS is to use the [pixi][pixi-link] package manager, in which case `pixi add aiida-fans` will install the plugin from conda-forge by default, as well as its dependencies: python, aiida-core, and h5py.

Otherwise, the package can be installed with pip by `pip install aiida-fans` or with mamba by `mamba install aiida-fans`.

In any case, the user is responsible for installing FANS and ensuring it is accessible to the plugin. This can be achieved without need for further customisation by having FANS accessible on the PATH environment variable. Please consult the [FANS repository][FANS-link] for more information on the installation of this software.

<!-- URLs -->

[FANS-link]: https://github.com/DataAnalyticsEngineering/FANS
[pixi-link]: https://pixi.sh/latest/
