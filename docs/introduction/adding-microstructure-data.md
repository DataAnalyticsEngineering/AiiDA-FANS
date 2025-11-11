# Adding Microstructure Data

A FANS calculation requires a microstructure dataset. You must create a node in your AiiDA profile that corresponds to such a microstructure. An example microstructure file is included in the accompanying tutorial which you can download with,

```sh
wget https://github.com/DataAnalyticsEngineering/AiiDA-FANS/raw/refs/heads/main/tutorial/ms-example.h5
```

Alternatively, you can visit the [FANS repository](https://github.com/DataAnalyticsEngineering/FANS) for more information and sample microstructures.

Since realistic microstructure files tend to be extremely big, saving such files in an AiiDA profile has some significant drawbacks. As such, you are required to put the microstructure file on the same machine as where you intend to run FANS. We recommend you locate it in the working directory of the AiiDA computer you created, within a subdirectory called "microstructures/".

Once you have a microstructure file, you must create a `RemoteData` node like so:

```python
from aiida import load_profile
from aiida.orm import RemoteData load_computer

load_profile()

COMPUTER_LABEL = "localhost"
MICROSTRUCTURE_PATH = "/path/to/microstructures/ms-example.h5"

RemoteData(
    remote_path=MICROSTRUCTURE_PATH,
    computer=load_computer(COMPUTER_LABEL),
    label="microstructure.file",
).store()
```

You can write this in a python script and run it, or use AiiDA's interactive shell with `verdi shell`. If you use the interactive shell, you can omit `load_profile` as AiiDA will automatically load the default profile. Remember to change `COMPUTER_LABEL` and `MICROSTRUCTURE_PATH` to the appropriate values.

After this, you can check the nodes on your profile with `verdi node list` and expose details of a particular node with `verdi node show <pk>`.
