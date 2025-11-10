# Usage

To use this plugin, you must first establish an AiiDA profile, computer, and code. For help on how to do this please refer to the [AiiDA installation][AiiDA-install-link] guide.

For general information on the usage of AiiDA you should refer to the [AiiDA documentation][AiiDA-docs-link], and for the usage of FANS refer to its [repository][FANS-link].

## Utilities

This plugin offers some utilities to help smooth the AiiDA user experience. Namely, the `utils.execute_fans` function which allows you to provide the inputs for a job as a dictionary of mostly pythonic values. This utility will parse these inputs and automatically use any appropriate existing nodes it finds in your profile before making new nodes where necessary.

<!-- URLs -->
[AiiDA-docs-link]: https://aiida-core.readthedocs.io/
[AiiDA-install-link]: https://aiida.readthedocs.io/projects/aiida-core/en/latest/installation/index.html
[FANS-link]: https://github.com/DataAnalyticsEngineering/FANS
