from amsdal_models.migration import migrations
from amsdal_utils.models.enums import ModuleType


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="Journey",
            old_schema={
                "title": "Journey",
                "properties": {
                    "start_date": {"type": "string", "title": "start_date"},
                    "end_date": {"type": "string", "title": "end_date"},
                    "country": {"type": "Country", "title": "country", "db_field": ["country_partition_key"]},
                    "equipment": {
                        "type": "dictionary",
                        "items": {"key": {"type": "string"}, "value": {"type": "number"}},
                        "title": "equipment",
                    },
                    "persons": {"type": "array", "items": {"type": "Person"}, "title": "persons"},
                    "bookings": {"type": "array", "items": {"type": "Booking"}, "title": "bookings"},
                },
                "custom_code": "from typing import Any\n\nfrom amsdal_models.builder.validators.dict_validators import validate_non_empty_keys\nfrom pydantic.functional_validators import field_validator\n\nfrom models.booking import *\nfrom models.country import *\nfrom models.person import *\n\n\n@field_validator('equipment')\n@classmethod\ndef _non_empty_keys_equipment(cls: type, value: Any) -> Any:\n    return validate_non_empty_keys(value)",
                "table_name": "Journey",
                "primary_key": ["partition_key"],
                "foreign_keys": {"country": [{"country_partition_key": "string"}, "Country", ["partition_key"]]},
            },
            new_schema={
                "title": "Journey",
                "properties": {
                    "start_date": {"type": "string", "title": "start_date"},
                    "end_date": {"type": "string", "title": "end_date"},
                    "country": {"type": "Country", "title": "country", "db_field": ["country_partition_key"]},
                    "equipment": {
                        "type": "dictionary",
                        "items": {"key": {"type": "string"}, "value": {"type": "number"}},
                        "title": "equipment",
                    },
                    "persons": {"type": "array", "items": {"type": "Person"}, "title": "persons"},
                    "bookings": {"type": "array", "items": {"type": "Booking"}, "title": "bookings"},
                },
                "custom_code": "from datetime import date, datetime\nfrom typing import Any\n\nfrom amsdal import Reference, ReferenceLoader\nfrom amsdal_models.builder.validators.dict_validators import validate_non_empty_keys\nfrom pydantic.functional_validators import field_validator\n\nfrom models.booking import *\nfrom models.country import *\nfrom models.person import *\n\n\n@field_validator('equipment')\n@classmethod\ndef _non_empty_keys_equipment(cls: type, value: Any) -> Any:\n    return validate_non_empty_keys(value)\n\ndef pre_create(self) -> None:\n    self.validate_persons_age()\n\ndef validate_persons_age(self) -> None:\n    from models.person import Person\n    for index, person_reference in enumerate(self.persons or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = ReferenceLoader(person_reference).load_reference()\n        else:\n            person = ReferenceLoader(Reference(**person_reference)).load_reference()\n        try:\n            birthdate = datetime.strptime(person.dob, '%Y-%m-%d')\n        except (TypeError, ValueError):\n            continue\n        today = date.today()\n        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n        if age < 18:\n            raise ValueError(f'{person.first_name} {person.last_name}: Age must be 18 or older')",
                "table_name": "Journey",
                "primary_key": ["partition_key"],
                "foreign_keys": {"country": [{"country_partition_key": "string"}, "Country", ["partition_key"]]},
            },
        ),
    ]
