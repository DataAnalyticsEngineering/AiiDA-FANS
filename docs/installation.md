# Installation

AiiDA-FANS is available on the conda-forge package channel. Our recommended method of installing AiiDA-FANS is to use the [Pixi][Pixi-link] package manager, in which case `pixi add aiida-fans` will add the plugin to your project manifest (such as a pyproject.toml).

Otherwise, the package can be installed with conda by `conda install aiida-fans --channel conda-forge`.

In any case, the user is responsible for installing FANS and ensuring it is accessible to the plugin. This can be achieved without need for further customisation by having FANS accessible on the PATH environment variable. Please consult the [FANS repository][FANS-link] for more information on the installation of this software.

<!-- URLs -->

[FANS-link]: https://github.com/DataAnalyticsEngineering/FANS
[Pixi-link]: https://pixi.sh/latest/
