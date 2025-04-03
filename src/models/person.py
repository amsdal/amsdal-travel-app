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

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.age} years old)"

    @property
    def age(self):
        from datetime import datetime
        from datetime import date

        today = date.today()

        try:
            birthdate = datetime.strptime(self.dob, "%Y-%m-%d")
        except (TypeError, ValueError):
            return "N/A"
        else:
            return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))