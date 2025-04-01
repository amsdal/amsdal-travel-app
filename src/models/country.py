from typing import ClassVar
from typing import Optional

from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field


class Country(Model):
    __module_type__: ClassVar[ModuleType] = ModuleType.USER
    name: Optional[str] = Field(None, title='name')
    code: Optional[str] = Field(None, title='code')
