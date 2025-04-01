from typing import Any
from typing import ClassVar
from typing import Optional

from amsdal_models.builder.validators.dict_validators import validate_non_empty_keys
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field
from pydantic.functional_validators import field_validator

from models.booking import *
from models.country import *
from models.person import *


class Journey(Model):
    __module_type__: ClassVar[ModuleType] = ModuleType.USER
    start_date: Optional[str] = Field(None, title='start_date')
    end_date: Optional[str] = Field(None, title='end_date')
    country: Optional['Country'] = Field(None, title='country')
    persons: Optional[list['Person']] = Field(None, title='persons')
    equipment: Optional[dict[str, Optional[float]]] = Field(None, title='equipment')
    bookings: Optional[list['Booking']] = Field(None, title='bookings')

    @field_validator('equipment')
    @classmethod
    def _non_empty_keys_equipment(cls: type, value: Any) -> Any:
        return validate_non_empty_keys(value)
