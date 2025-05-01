"""Utilities provided by aiida_fans."""

from typing import Any, Literal

from aiida import load_profile  # type: ignore
from aiida.orm import Code, SinglefileData


def submit_fans(  # noqa: PLR0913
        code: Code,
        microstructure: SinglefileData,
        inputs: dict[str, Any],
        metadata: dict[str, Any] | None = None,
        mode: Literal["Fragmented", "Stashed"] = "Fragmented",
        profile: str | None = None
    ):
    """This utility function simplifies the process of submitting jobs to aiida-fans.

    The only nodes you must provide are the code and microstructure. Other inputs
    can be given as standard python variables. Your repository will be automatically
    scanned for equivalent nodes. These will be used whenever possible, otherwise
    new nodes will be created.

    Args:
        code (Code)
        microstructure (SinglefileData)
        inputs (dict[str, Any])
        metadata (dict[str, Any])
        mode (Literal["Fragmented", "Stashed"])
        profile (str | None, optional): The name of the profile you wish to use.
            Omit to use your default profile. Defaults to None.
    """
    load_profile(profile)
    pass
