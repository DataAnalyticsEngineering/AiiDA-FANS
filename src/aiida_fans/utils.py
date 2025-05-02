"""Utilities provided by aiida_fans."""

from pathlib import Path
from typing import Any, Literal

from aiida.common.datastructures import StashMode
from aiida.engine import submit, run
from aiida.orm import load_node
from aiida.plugins import CalculationFactory

# load_node(label="microstructure")


def submit_fans(
        inputs: dict[str, Any],
        strategy: Literal["Fragmented", "Stashed"] = "Fragmented",
    ):
    """This utility function simplifies the process of submitting jobs to aiida-fans.

    The only nodes you must provide are the `code` and `microstructure` inputs.
    Other inputs can be given as standard python variables. Your repository will
    be automatically scanned for equivalent nodes. These will be used whenever
    possible, otherwise new nodes will be created.

    The `strategy` specifies which microstructure distribution method you wish to use.
    It defaults to "Fragmented". When using the stashed method, you must ensure
    to include the appropriate `metadata.options` along with your inputs.

    You must load an AiiDA profile yourself before using this function.

    **Args:**
        **inputs** *(dict[str, Any])*
        **strategy** *(Literal["Fragmented", "Stashed"]), optional*

    ---

    **Example:**
    ```
    from aiida import load_profile
    from aiida.orm import load_code, load_node
    from aiida_fans.utils import submit_fans
    load_profile()
    inputs = {
        "code": load_code("fans"),
        "microstructure": load_node(label="microstructure"),
        ...
        "metadata": {
            "label": "an example calculation"
        }
    }
    submit_fans(inputs, "Stashed")
    ```
    """
    # update inputs with metadata.options.stash if necessary:
    if strategy == "Fragmented":
        calcjob = CalculationFactory("fans.fragmented")
        # if inputs["metadata"]["options"].get("stash") is not None:
        #     print("WARNING: Fragmented calculation strategy may operate incorrectly with extraneous stash options.")
    elif strategy == "Stashed":
        calcjob = CalculationFactory("fans.stashed")
        # if the stash already exists,
        # if (
        #     Path(inputs["code"].computer.get_workdir()) /
        #     "stash/microstructures" /
        #     inputs["microstructure"]["file"].filename
        # ).is_file():
        #     # if stash options are given, warn
        #     if inputs["metadata"]["options"].get("stash") is not None:
        #         print("WARNING: Stashed calculation strategy may operate incorrectly with extraneous stash options.")
        # # if the stash does NOT already exist,
        # else:  # noqa: PLR5501
        #     # if stash options are not given, make them
        #     # if (inputs["metadata"].get("options") is None) or (inputs["metadata"]["options"].get("stash") is None):
        #     if inputs["metadata"].get("options", {}).get("stash") is None:
        #         if inputs["metadata"].get("options") is None:
        #             inputs["metadata"]["options"] = {}
        #         inputs["metadata"]["options"].update( { "stash": {
        #             "source_list": [inputs["microstructure"]["file"].filename],
        #             "target_base": str(Path(inputs["code"].computer.get_workdir()) / "stash/microstructures"),
        #             "stash_mode": StashMode.COPY.value,
        #         } } )
        #     # if stash options ARE given, warn
        #     else:
        #         print("WARNING: Stashed calculation strategy is incompatible with extraneous stash options.")
    else:
        print("ERROR: Calculation strategy must be either 'Fragmented' or 'Stashed'.")
        raise ValueError

    # fetch the inputs if possible or otherwise create them
    pass

    run(calcjob, inputs)
