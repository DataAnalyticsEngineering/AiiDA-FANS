"""This is an example submit script. It should **not** be committed to dev."""

from aiida import load_profile  # type: ignore
from aiida.orm import load_code, load_node
from aiida.tools import delete_nodes

from aiida_fans.utils import run_fans

load_profile()


################################################################################

inputs = {
    "code": load_code("FANS"),  #! Code node goes here.
    "microstructure": {
        "file": load_node(label="microstructure.file"),  #! Microstructure node goes here.
        "datasetname": "/dset_0/image",
        "L": [1.0, 1.0, 1.0]
    },
    "results_prefix": "my_results",  #? Optional
    "problem_type": "mechanical",
    "matmodel": "LinearElasticIsotropic",

    ######################################
    # Proposed material properties format:
    "material_phases": {
        "copper": [0, 2],
        "aluminium": [1]
    },
    # translates to: phase 0 = copper, phase 1 = aluminium, phase 2 = copper
    #
    # Under this format, each material would be its own node labelled "copper",
    # "aluminium", etc., and they would be of various MaterialData types that
    # the plugin defines for each supported matmodel.
    #
    # Additionally, each job would have a material_phases input which defines
    # what materials occupy which phases of the microstructure. If the user were
    # to provide materials inconsistent with the provided "matmodel", utils
    # could reject the input without ever calling AiiDA or FANS.
    #
    # If an advanced user wishes to use a custom material, they must create the
    # node themselves and provide it a unique label. That label can then simply
    # be used in place of "copper" or "alumininum" above.
    ######################################

    "method": "cg",
    "error_parameters": {
        "measure": "Linfinity",
        "type": "absolute",
        "tolerance": 1e-10
    },
    "n_it": 100,
    "macroscale_loading": [
        {
            "strain_indices": [      2, 3, 4, 5],
            "stress_indices": [0, 1            ],
            "strain": [[0.005, 0.0, 0.0, 0.0],[0.010, 0.0, 0.0, 0.0]],
            "stress": [[0.0, 0.0],[0.0, 0.0]]
        },
        {
            "strain_indices": [            4, 5],
            "stress_indices": [0, 1, 2, 3      ],
            "strain": [[0.001, 0.005],[0.005, 0.001]],
            "stress": [[0.01, 0.0, 0.0, 0.0],[0.0, 0.01, 0.0, 0.0]]
        }
    ],
    "results": [  # Optional
        "stress", "strain",
        "stress_average", "strain_average",
        "phase_stress_average", "phase_strain_average",
        "microstructure", "displacement", "absolute_error",
    ],

    "metadata": {  # Optional
        # "label": "test calculation 1",
        # "dry_run": True
    }
}

################################################################################

run_fans(inputs)
