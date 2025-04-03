from typing import Any
from typing import ClassVar
from typing import Optional

from amsdal import Reference
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
    start_timestamp: Optional[float] = Field(None, title='start_timestamp')
    end_date: Optional[str] = Field(None, title='end_date')
    country: Optional['Country'] = Field(None, title='country')
    persons: Optional[list['Person']] = Field(None, title='persons')
    equipment: Optional[dict[str, Optional[float]]] = Field(None, title='equipment')
    bookings: Optional[list['Booking']] = Field(None, title='bookings')

    @field_validator('equipment')
    @classmethod
    def _non_empty_keys_equipment(cls: type, value: Any) -> Any:
        return validate_non_empty_keys(value)

    async def apre_create(self) -> None:
        await self.validate_persons_age()

    async def validate_persons_age(self) -> None:
        from models.person import Person

        for index, person_reference in enumerate(self.persons or []):
            person: Person

            if isinstance(person_reference, Person):
                person = person_reference
            elif isinstance(person_reference, Reference):
                person = await person_reference
            else:
                person = await Reference(**person_reference)

            if person.age == "N/A":
                raise ValueError("Invalid DOB format. Please use YYYY-MM-DD")

            if person.age < 18:
                raise ValueError(
                    f"{person.first_name} {person.last_name}: Age must be 18 or older"
                )

    def post_init(self, is_new_object, kwargs):
        from datetime import datetime

        try:
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
        except (TypeError, ValueError):
            self.start_timestamp = None
        else:
            self.start_timestamp = start_date.timestamp()