# AiiDA-FANS

[![Release][release-badge]][release-link]
[![Downloads][conda-badge]][conda-link]
[![License][license-badge]][license-link]
[![Docs Status][docs-badge]][docs-link]

> [!WARNING]  
> The AiiDA-Fans plugin is under active development. Changes can and do occur regularly.

This is a plugin for [AiiDA][AiiDA-link] that facilitates the use of [FANS][FANS-link]. FANS is an FFT-based homogenisation solver for microscale and multiphysics problems. It is an open-source project under active development at the Institute of Applied Mechanics, University of Stuttgart. This plugin aims to bring the full value of provenance tracking and database integration to the results produced by FANS.

The design goals of this plugin are to provide a simple but powerful user interface to FANS. In doing so, the plugin packages additional utilities to eliviate some of the burdens we perceive in the traditional AiiDA workflow.

## Installation

AiiDA-FANS is available on the conda-forge package channel. Our recommended method of installing AiiDA-FANS is to use the [Pixi][Pixi-link] package manager, in which case `pixi add aiida-fans` will add the plugin to your project manifest (such as a pyproject.toml).

Otherwise, the package can be installed with conda by `conda install aiida-fans --channel conda-forge`.

In any case, the user is responsible for installing FANS and ensuring it is accessible to the plugin. This can be achieved without need for further customisation by having FANS accessible on the PATH environment variable. Please consult the [FANS repository][FANS-link] for more information on the installation of this software.

## Usage

To use this plugin, you must first establish an AiiDA profile, computer, and code. For help on how to do this please refer to the [AiiDA installation][AiiDA-install-link] guide.

For general information on the usage of AiiDA you should refer to the [AiiDA documentation][AiiDA-docs-link], and for the usage of FANS refer to its [repository][FANS-link].

This plugin offers some utilities to help smooth the AiiDA user experience. Namely, the `utils.execute_fans` function which allows you to provide the inputs for a job as a dictionary of mostly pythonic values. This utility will parse these inputs and automatically use any appropriate existing nodes it finds in your profile before making new nodes where necessary. For more information on this plugin's specifics and how to use the utilities, please refer to the [documentation][docs-link].

## Tutorial

A tutorial accompanies this plugin. To try it out: clone this repository, cd into it, run `pixi shell -e tutorial` and `pixi run tutorial`. The marimo notebook should be served locally. For more information before you begin, take a look at the [documentation][tutorial-docs-link].

## Contact

You can contact <ethan.shanahan@gmail.com> with any questions regarding the AiiDA-FANS plugin and accompanying tutorial.

<!-- URLs -->
[release-badge]: https://img.shields.io/github/v/release/dataanalyticsengineering/AiiDA-FANS?label=Release
[release-link]: https://github.com/dataanalyticsengineering/AiiDA-FANS/releases/latest
[conda-badge]: https://img.shields.io/conda/dn/conda-forge/aiida-fans?label=Downloads
[conda-link]: https://anaconda.org/conda-forge/aiida-fans
[license-badge]: https://img.shields.io/github/license/ethan-shanahan/pokemanager?label=License
[license-link]: https://www.gnu.org/licenses/lgpl-3.0.en.html
[docs-badge]: https://github.com/dataanalyticsengineering/AiiDA-FANS/actions/workflows/docs.yml/badge.svg
[docs-link]: https://dataanalyticsengineering.github.io/AiiDA-FANS/

[tutorial-docs-link]: https://dataanalyticsengineering.github.io/AiiDA-FANS/tutorial/installation/
[AiiDA-link]: https://www.aiida.net/
[AiiDA-docs-link]: https://aiida-core.readthedocs.io/
[AiiDA-install-link]: https://aiida.readthedocs.io/projects/aiida-core/en/latest/installation/index.html
[FANS-link]: https://github.com/DataAnalyticsEngineering/FANS
[Pixi-link]: https://pixi.sh/latest/
