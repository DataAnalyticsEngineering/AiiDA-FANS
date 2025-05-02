"""Calculations provided by aiida_fans."""

from json import dump
from pathlib import Path
from shutil import copyfileobj
from typing import Any, Callable

import h5py
from aiida.common.datastructures import CalcInfo, CodeInfo, StashMode
from aiida.common.folders import Folder
from aiida.engine import CalcJob
from aiida.engine.processes.process_spec import CalcJobProcessSpec
from aiida.orm import ArrayData, Dict, Float, Int, List, SinglefileData, Str
from plumpy.utils import AttributesFrozendict

from aiida_fans.helpers import InputEncoder


class FansFragmentedCalculation(CalcJob):
    """AiiDA calculation plugin wrapping the FANS executable.

    The microstructure file is fragmented as necessary by individual jobs,
    copying the relevant dataset to the working directory.
    """
    pass

class FansStashedCalculation(CalcJob):
    """AiiDA calculation plugin wrapping the FANS executable.

    The microstructure file is stashed on the working machine in a consistent
    location and read by many jobs at once.
    """

    @classmethod
    def define(cls, spec: CalcJobProcessSpec) -> None:
        """Define inputs, outputs, and exit_codes of the calculation."""
        super().define(spec)

        # Metadata
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 4,
        }
        spec.inputs["metadata"]["options"]["withmpi"].default = True
        spec.inputs["metadata"]["options"]["parser_name"].default = "fans"
        spec.inputs["metadata"]["options"]["input_filename"].default = "input.json"
        spec.inputs["metadata"]["options"]["output_filename"].default = "output.h5"

        # Ports
        spec.input_namespace("microstructure")
        spec.input("microstructure.file", valid_type=SinglefileData)
        spec.input("microstructure.datasetname", valid_type=Str)
        spec.input("microstructure.L", valid_type=List)
        spec.input("problem_type", valid_type=Str)
        spec.input("matmodel", valid_type=Str)
        spec.input("material_properties", valid_type=Dict)
        spec.input("method", valid_type=Str)
        spec.input_namespace("error_parameters")
        spec.input("error_parameters.measure", valid_type=Str)
        spec.input("error_parameters.type", valid_type=Str)
        spec.input("error_parameters.tolerance", valid_type=Float)
        spec.input("n_it", valid_type=Int)
        spec.input("macroscale_loading", valid_type=ArrayData)
        spec.input("results", valid_type=List)

        spec.output("results", valid_type=SinglefileData)

        spec.exit_code(400, "PLACEHOLDER", "This is an error code, yet to be implemented.")

    def prepare_for_submission(self, folder: Folder) -> CalcInfo:
        """Prepare the calcjob for submission."""
        # locating/stashing the microstucture file
        ms_filename: str = self.inputs.microstructure.file.filename
        ms_filepath: Path = Path(self.inputs.code.computer.get_workdir()) / "stash/microstructures" / ms_filename

        if not ms_filepath.is_file():
            ms_filepath.parent.mkdir(parents=True, exist_ok=True)
            with self.inputs.microstructure.file.open(mode='rb') as source:
                with ms_filepath.open(mode='wb') as target:
                    copyfileobj(source, target)

        assert ms_filepath.is_file()

        json_to_be = {
            "ms_filename": str(ms_filepath),
            "ms_datasetname": self.inputs.microstructure.datasetname.value,
            "ms_L": self.inputs.microstructure.L.get_list(),
            "problem_type": self.inputs.problem_type.value,
            "matmodel": self.inputs.matmodel.value,
            "material_properties": self.inputs.material_properties.get_dict(),
            "method": self.inputs.method.value,
            "error_parameters": {
                "measure": self.inputs.error_parameters.measure.value,
                "type": self.inputs.error_parameters.type.value,
                "tolerance": self.inputs.error_parameters.tolerance.value
            },
            "n_it": self.inputs.n_it.value,
            "macroscale_loading": [a[1].tolist() for a in self.inputs.macroscale_loading.get_iterarrays()],
            "results": self.inputs.results.get_list()
        }

        with folder.open(self.options.input_filename, "w", "utf8") as dest:
            dump(json_to_be, dest, indent=4)

        # Specifying code info.
        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.options.input_filename + ".log"
        codeinfo.stderr_name = self.options.input_filename + ".err"
        codeinfo.cmdline_params = [self.options.input_filename, self.options.output_filename]

        # Specifying calc info.
        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = []
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [
            self.options.input_filename + ".log",
            self.options.input_filename + ".err",
        ]
        calcinfo.retrieve_temporary_list = [
            self.options.output_filename
        ]

        return calcinfo



class FansCalculation(CalcJob):
    """AiiDA calculation plugin wrapping the FANS executable."""

    @staticmethod
    def __input_validator_selector(input: str, note: str) -> Callable[[Any, Any], str | None]:
        validators: dict[str, Callable[[Any, Any], str | None]] = {
            "microstructure.file": lambda _i, _p: None,
            "microstructure.datasetname": lambda _i, _p: None,
            "microstructure.L": lambda i, _p: note if len(i) != 3 else None,  # TODO: check elements are numbers
            "problem_type": lambda i, _p: note if i.value not in {"thermal", "mechanical"} else None,
            "matmodel": lambda i, _p: note
            if i.value
            not in {
                "LinearThermalIsotropic",
                "LinearElasticIsotropic",
                "PseudoPlasticLinearHardening",
                "PseudoPlasticNonLinearHardening",
                "J2ViscoPlastic_LinearIsotropicHardening",
                "J2ViscoPlastic_NonLinearIsotropicHardening",
            }
            else None,
            "material_properties": lambda _i, _p: None,  # TODO: material properties
            "method": lambda i, _p: note if i.value not in {"cg", "fp"} else None,
            "error_parameters.measure": lambda i, _p: note if i.value not in {"Linfinity", "L1", "L2"} else None,
            "error_parameters.type": lambda i, _p: note if i.value not in {"absolute", "relative"} else None,
            "error_parameters.tolerance": lambda _i, _p: None,
            "n_it": lambda _i, _p: None,
            "macroscale_loading": lambda _i, _p: None,  # TODO: macroscale loading
            "results": lambda i, _p: note
            if not set(i.get_list())
            <= {
                "stress_average",
                "strain_average",
                "absolute_error",
                "phase_stress_average",
                "phase_strain_average",
                "microstructure",
                "displacement",
                "stress",
                "strain",
            }
            else None,
        }
        return validators[input]

    @classmethod
    def define(cls, spec: CalcJobProcessSpec) -> None:
        """Define inputs, outputs, and exit_codes of the calculation."""
        super().define(spec)

        # Metadata
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 4,
        }
        spec.inputs["metadata"]["options"]["withmpi"].default = True
        spec.inputs["metadata"]["options"]["parser_name"].default = "fans"
        spec.inputs["metadata"]["options"]["input_filename"].default = "input.json"
        spec.inputs["metadata"]["options"]["output_filename"].default = "output.h5"
        ## Stash
        spec.inputs["metadata"]["options"]["stash"].default = {
            "source_list": "microstructure.h5",
            "target_base": str(Path.home()) + "/aiida_stash/" + spec.inputs["microstructure"]["datasetname"].value,
            "stash_mode": StashMode.COPY.value,
        }
        # spec.inputs["metadata"]["options"]["stash"]["source_list"].default = "?"
        # spec.inputs["metadata"]["options"]["stash"]["target_base"].default = "?"
        # spec.inputs["metadata"]["options"]["stash"]["stash_mode"].default = StashMode

        # New Ports:
        spec.input_namespace("microstructure", help=(note := "The microstructure definition."))
        spec.input(
            (input := "microstructure.file"),
            valid_type=SinglefileData,
            validator=cls.__input_validator_selector(input, note),
            help=(note := "This specifies the path to the HDF5 file that contains the microstructure data."),
        )
        spec.input(
            (input := "microstructure.datasetname"),
            valid_type=Str,
            validator=cls.__input_validator_selector(input, note),
            help=(
                note
                := "This is the path within the HDF5 file to the specific dataset that represents the microstructure."
            ),
        )
        spec.input(
            (input := "microstructure.L"),
            valid_type=List,
            validator=cls.__input_validator_selector(input, note),
            help=(
                note
                := "Microstructure length defines the physical dimensions of the microstructure in the x, y, and z directions."  # noqa: E501
            ),
        )

        spec.input(
            (input := "problem_type"),
            valid_type=Str,
            validator=cls.__input_validator_selector(input, note),
            help=(
                note
                := "This defines the type of physical problem you are solving. Common options include `thermal` problems and `mechanical` problems."  # noqa: E501
            ),
        )
        spec.input(
            (input := "matmodel"),
            valid_type=Str,
            validator=cls.__input_validator_selector(input, note),
            help=(note := "This specifies the material model to be used in the simulation."),
        )
        spec.input(
            (input := "material_properties"),
            valid_type=Dict,
            validator=cls.__input_validator_selector(input, note),
            help=(note := "This provides the necessary material parameters for the chosen material model."),
        )
        spec.input(
            (input := "method"),
            valid_type=Str,
            validator=cls.__input_validator_selector(input, note),
            help=(
                note
                := "This indicates the numerical method to be used for solving the system of equations. `cg` stands for the Conjugate Gradient method, and `fp` stands for the Fixed Point method."  # noqa: E501
            ),
        )

        spec.input_namespace(
            "error_parameters",
            help=(
                note
                := "This section defines the error parameters for the solver. Error control is applied on the finite element nodal residual of the problem."  # noqa: E501
            ),
        )
        spec.input(
            (input := "error_parameters.measure"),
            valid_type=Str,
            validator=cls.__input_validator_selector(input, note),
            help=(note := "Specifies the norm used to measure the error. Options include `Linfinity`, `L1`, or `L2`."),
        )
        spec.input(
            (input := "error_parameters.type"),
            valid_type=Str,
            validator=cls.__input_validator_selector(input, note),
            help=(note := "Defines the type of error measurement. Options are `absolute` or `relative`."),
        )
        spec.input(
            (input := "error_parameters.tolerance"),
            valid_type=Float,
            validator=cls.__input_validator_selector(input, note),
            help=(
                note
                := "Sets the tolerance level for the solver, defining the convergence criterion based on the chosen error measure. The solver iterates until the solution meets this tolerance."  # noqa: E501
            ),
        )

        spec.input(
            (input := "n_it"),
            valid_type=Int,
            validator=cls.__input_validator_selector(input, note),
            help=(note := "Specifies the maximum number of iterations allowed for the FANS solver."),
        )
        spec.input(
            (input := "macroscale_loading"),
            valid_type=ArrayData,
            validator=cls.__input_validator_selector(input, note),
            help=(
                note
                := "This defines the external loading applied to the microstructure. It is an array of arrays, where each sub-array represents a loading condition applied to the system. The format of the loading array depends on the problem type."  # noqa: E501
            ),
        )
        spec.input(
            (input := "results"),
            valid_type=List,
            validator=cls.__input_validator_selector(input, note),
            help=(
                note
                := "This array lists the quantities that should be stored into the results HDF5 file during the simulation."  # noqa: E501
            ),
        )

        spec.output("results", valid_type=SinglefileData)

        # Exit Codes:
        spec.exit_code(400, "PLACEHOLDER", "This is an error code, yet to be implemented.")

    def prepare_for_submission(self, folder: Folder) -> CalcInfo:
        """Creates the input file required by the calculation.

        Args:
            folder (Folder): where the plugin should temporarily place all files needed by the calculation

        Returns:
            CalcInfo: the data to be passed to the ExecManager
        """
        # Write Microstructure Subset to Folder
        datasetname : str = self.inputs.microstructure.datasetname.value
        with folder.open("microstructure.h5","bw") as f_dest:
            with h5py.File(f_dest,"w") as h5_dest:
                with self.inputs.microstructure.file.open(mode="rb") as f_src:
                    with h5py.File(f_src,'r') as h5_src:
                        h5_src.copy(datasetname, h5_dest, name=datasetname)

        # Write input.json to Folder
        json_to_be = dict(self.inputs)
        del json_to_be["code"], json_to_be["metadata"]
        to_fix = {}
        for key, value in json_to_be.items():
            if isinstance(value, AttributesFrozendict):  # can be moved to InputEncoder?
                to_fix[key] = {}
                for k, v in json_to_be[key].items():
                    to_fix[key][k] = v
        json_to_be = json_to_be | to_fix

        to_add = {}
        for key, value in json_to_be.items():
            if key == "microstructure":
                for k, v in value.items():
                    if k == "file":
                        to_add[f"ms_{k}name"] = "microstructure.h5"
                    else:
                        to_add[f"ms_{k}"] = v

        json_to_be = to_add | json_to_be
        del json_to_be["microstructure"]

        with folder.open(self.options.input_filename, "w", "utf8") as handle:
            dump(json_to_be, handle, cls=InputEncoder, indent=4)

        # Specifying code info.
        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.options.input_filename + ".log"
        codeinfo.stderr_name = self.options.input_filename + ".err"
        codeinfo.cmdline_params = [self.options.input_filename, self.options.output_filename]

        # Specifying calc info.
        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = []
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [
            self.options.input_filename + ".log",
            self.options.input_filename + ".err",
        ]
        calcinfo.retrieve_temporary_list = [
            self.options.output_filename
        ]
        calcinfo.provenance_exclude_list = [
            "microstructure.h5"
        ]

        return calcinfo
