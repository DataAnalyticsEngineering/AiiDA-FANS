"""Subclasses of Data for aiida-fans."""

from aiida.orm import Data


class MaterialData(Data):
    """Data class to represent material properties."""

    def __init__(self, **kwargs):
        """Initialize the MaterialData instance."""
        bulk = kwargs.pop("bulk_modulus", None)
        shear = kwargs.pop("shear_modulus", None)
        super().__init__(**kwargs)
        if bulk is not None:
            self.base.attributes.set("bulk_modulus", bulk)
        if shear is not None:
            self.base.attributes.set("shear_modulus", shear)
