# Getting Started

To use AiiDA-FANS, you need to take the following first steps.

- Install FANS.
- Install AiiDA version 2.X on the same machine, or another that can ssh to the machine, with FANS.
- Install AiiDA-FANS in the same environment as AiiDA.
- Setup an AiiDA [profile](https://aiida.readthedocs.io/projects/aiida-core/en/stable/installation/guide_complete.html#create-a-profile).
- Setup a [computer](https://aiida.readthedocs.io/projects/aiida-core/en/stable/howto/run_codes.html#how-to-set-up-a-computer) for the machine you intend to run FANS on.
- Setup a [code](https://aiida.readthedocs.io/projects/aiida-core/en/stable/howto/run_codes.html#how-to-create-a-code) using `default_calc_job_plugin: fans` config.

AiiDA often undergoes significant changes, so for details on how to accomplish many of these steps you should refer to the [AiiDA docs](https://aiida.readthedocs.io/projects/aiida-core/en/stable/) for the latest information or the accompanying [tutorial](../tutorial/installing-the-tutorial.md) for details on a specific version of AiiDA that is likely still relevant.

FANS is a simple program to install via conda-forge. You can find out more about it, including alternative installation methods, on the [FANS repository](https://github.com/DataAnalyticsEngineering/FANS). You should consider installing FANS on a HPC to get the fullest out of its capabilities, and allowing AiiDA to [access it via ssh](https://aiida.readthedocs.io/projects/aiida-core/en/stable/howto/ssh.html).
