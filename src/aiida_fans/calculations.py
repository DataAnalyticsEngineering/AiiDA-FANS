"""CalcJob subclasses for aiida-fans calculations."""

from json import dump
from pathlib import Path
from shutil import copyfileobj

from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.common.folders import Folder
from aiida.engine import CalcJob
from aiida.engine.processes.process_spec import CalcJobProcessSpec
from aiida.orm import Dict, Float, Int, List, SinglefileData, Str
from h5py import File as h5File

from aiida_fans.helpers import make_input_dict


class FansCalculation(CalcJob):
    """Calculations using FANS."""

    @classmethod
    def define(cls, spec: CalcJobProcessSpec) -> None:
        """Define inputs, outputs, and exit codes of the calculation."""
        super().define(spec)

        # Default Metadata
        spec.inputs["metadata"]["label"].default = "FANS"
        ## Processing Power
        spec.inputs["metadata"]["options"]["withmpi"].default = True
        spec.inputs["metadata"]["options"]["resources"].default = {"num_machines": 1, "num_mpiprocs_per_machine": 4}
        ## Filenames
        spec.inputs["metadata"]["options"]["input_filename"].default = "input.json"
        spec.inputs["metadata"]["options"]["output_filename"].default = "output.h5"
        ## Parser
        spec.inputs["metadata"]["options"]["parser_name"].default = "fans"

        # Custom Metadata
        spec.input("metadata.options.results_prefix", valid_type=str, default="")
        spec.input("metadata.options.results", valid_type=list, default=[])
        spec.input("metadata.options.stashed_microstructure", valid_type=bool, default=True)

        # Input Ports
        ## Microstructure Definition
        spec.input_namespace("microstructure")
        spec.input("microstructure.file", valid_type=SinglefileData)
        spec.input("microstructure.datasetname", valid_type=Str)
        spec.input("microstructure.L", valid_type=List)
        ## Problem Type and Material Model
        spec.input("problem_type", valid_type=Str)
        spec.input("matmodel", valid_type=Str)
        spec.input("material_properties", valid_type=Dict)
        ## Solver Settings
        spec.input("method", valid_type=Str)
        spec.input("n_it", valid_type=Int)
        spec.input_namespace("error_parameters")
        spec.input("error_parameters.measure", valid_type=Str)
        spec.input("error_parameters.type", valid_type=Str)
        spec.input("error_parameters.tolerance", valid_type=Float)
        ## Macroscale Loading Conditions
        spec.input("macroscale_loading", valid_type=List)

        # Output Ports
        spec.output("output", valid_type=SinglefileData)
        spec.output("results", valid_type=Dict, required=False)

        # Exit Codes
        spec.exit_code(400, "PLACEHOLDER", "This is an error code, yet to be implemented.")

    def prepare_for_submission(self, folder: Folder) -> CalcInfo:
        """Prepare the calculation for submission."""
        # Stashed Strategy:
        if self.options.stashed_microstructure:
            ms_filepath: Path = (
                Path(self.inputs.code.computer.get_workdir())
                / "stash/microstructures"
                / self.inputs.microstructure.file.filename
            )
            # if microstructure does not exist in stash, make it
            if not ms_filepath.is_file():
                ms_filepath.parent.mkdir(parents=True, exist_ok=True)
                with self.inputs.microstructure.file.open(mode="rb") as source:
                    with ms_filepath.open(mode="wb") as target:
                        copyfileobj(source, target)

            # input.json as dict
            input_dict = make_input_dict(self)
            input_dict["microstructure"]["filepath"] = str(ms_filepath)
            # write input.json to working directory
            with folder.open(self.options.input_filename, "w", "utf8") as json:
                dump(input_dict, json, indent=4)
        # Fragmented Strategy:
        else:
            datasetname: str = self.inputs.microstructure.datasetname.value
            with folder.open("microstructure.h5", "bw") as f_dest:
                with h5File(f_dest, "w") as h5_dest:
                    with self.inputs.microstructure.file.open(mode="rb") as f_src:
                        with h5File(f_src, "r") as h5_src:
                            h5_src.copy(datasetname, h5_dest, name=datasetname)

            # input.json as dict
            input_dict = make_input_dict(self)
            input_dict["microstructure"]["filepath"] = "microstructure.h5"
            # write input.json to working directory
            with folder.open(self.options.input_filename, "w", "utf8") as json:
                dump(input_dict, json, indent=4)

        # Specifying the code info:
        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.label + ".log"
        codeinfo.stderr_name = self.metadata.label + ".err"
        codeinfo.cmdline_params = [self.options.input_filename, self.options.output_filename]

        # Specifying the calc info:
        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = []
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [codeinfo.stdout_name, codeinfo.stderr_name]
        calcinfo.retrieve_temporary_list = [self.options.output_filename]

        return calcinfo
