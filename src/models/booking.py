from typing import ClassVar
from typing import Optional

from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field

from models.property import *


class Booking(Model):
    __module_type__: ClassVar[ModuleType] = ModuleType.USER
    property: Optional['Property'] = Field(None, title='property')
    date: Optional[str] = Field(None, title='date')
    nights: Optional[float] = Field(1.0, title='nights')
