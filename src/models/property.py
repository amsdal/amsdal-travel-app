from typing import ClassVar
from typing import Optional

from amsdal.models.core.file import *
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field


class Property(Model):
    __module_type__: ClassVar[ModuleType] = ModuleType.USER
    name: Optional[str] = Field(None, title='name')
    type: Optional[str] = Field(None, title='type')
    address: Optional[str] = Field(None, title='address')
    free_parking: Optional[bool] = Field(None, title='free_parking')
    free_wifi: Optional[bool] = Field(None, title='free_wifi')
    photos: Optional[list['File']] = Field(None, title='photos')
