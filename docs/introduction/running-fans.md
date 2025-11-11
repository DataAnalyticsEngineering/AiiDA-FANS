# Running FANS

In this section, we will briefly demonstrate how to use the plugin's special utilities to easily run a FANS calculation. For general information on the usage of AiiDA you should refer to the [AiiDA documentation](https://aiida-core.readthedocs.io/), and for the usage of FANS refer to its [repository](https://github.com/DataAnalyticsEngineering/FANS).

## Utilities

This plugin offers some utilities to help smooth the AiiDA user experience. Namely, the `utils.execute_fans` function which allows you to provide the inputs for a job as a dictionary of mostly pythonic values. This utility will parse these inputs and automatically use any appropriate existing nodes it finds in your profile before making new nodes where necessary.
