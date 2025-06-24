"""Tools required by aiida-fans."""

from typing import Any

from aiida.engine import CalcJob
from numpy import allclose, ndarray


def make_input_dict(job: CalcJob) -> dict[str, Any]:
    """Prepares a dictionary that maps to an input.json from calcjob inputs."""
    return {
        ## Microstructure Definition
        "microstructure": {
            "filepath": None,  # path to stashed microstructure, must be overwritten by impl
            "datasetname": job.inputs.microstructure.datasetname.value,
            "L": job.inputs.microstructure.L.get_list(),
        },
        "results_prefix": job.inputs.metadata.options.results_prefix,
        ## Problem Type and Material Model
        "problem_type": job.inputs.problem_type.value,
        "matmodel": job.inputs.matmodel.value,
        "material_properties": job.inputs.material_properties.get_dict(),
        ## Solver Settings
        "method": job.inputs.method.value,
        "n_it": job.inputs.n_it.value,
        "error_parameters": {
            "measure": job.inputs.error_parameters.measure.value,
            "type": job.inputs.error_parameters.type.value,
            "tolerance": job.inputs.error_parameters.tolerance.value,
        },
        ## Macroscale Loading Conditions
        "macroscale_loading": job.inputs.macroscale_loading.get_list(),
        ## Results Specification
        "results": job.inputs.metadata.options.results,
    }


def arraydata_equal(first: dict[str, ndarray], second: dict[str, ndarray]) -> bool:
    """Return whether two dicts of arrays are roughly equal."""
    if first.keys() != second.keys():
        return False
    return all(allclose(first[key], second[key]) for key in first)
