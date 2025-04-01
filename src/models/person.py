from typing import ClassVar
from typing import Optional

from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field


class Person(Model):
    __module_type__: ClassVar[ModuleType] = ModuleType.USER
    first_name: Optional[str] = Field(None, title='first_name')
    last_name: Optional[str] = Field(None, title='last_name')
    dob: Optional[str] = Field(None, title='dob')
