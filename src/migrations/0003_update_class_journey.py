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
                "custom_code": "from datetime import date, datetime\nfrom typing import Any\n\nfrom amsdal import Reference\nfrom amsdal_models.builder.validators.dict_validators import validate_non_empty_keys\nfrom pydantic.functional_validators import field_validator\n\nfrom models.booking import *\nfrom models.country import *\nfrom models.person import *\n\n\n@field_validator('equipment')\n@classmethod\ndef _non_empty_keys_equipment(cls: type, value: Any) -> Any:\n    return validate_non_empty_keys(value)\n\nasync def apre_create(self) -> None:\n    await self.validate_persons_age()\n\nasync def validate_persons_age(self) -> None:\n    from models.person import Person\n    for index, person_reference in enumerate(self.persons or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = await person_reference\n        else:\n            person = await Reference(**person_reference)\n        try:\n            birthdate = datetime.strptime(person.dob, '%Y-%m-%d')\n        except (TypeError, ValueError):\n            continue\n        today = date.today()\n        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n        if age < 18:\n            raise ValueError(f'{person.first_name} {person.last_name}: Age must be 18 or older')",
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
                "custom_code": "from typing import Any\n\nfrom amsdal import Reference\nfrom amsdal_models.builder.validators.dict_validators import validate_non_empty_keys\nfrom pydantic.functional_validators import field_validator\n\nfrom models.booking import *\nfrom models.country import *\nfrom models.person import *\n\n\n@field_validator('equipment')\n@classmethod\ndef _non_empty_keys_equipment(cls: type, value: Any) -> Any:\n    return validate_non_empty_keys(value)\n\nasync def apre_create(self) -> None:\n    await self.validate_persons_age()\n\nasync def validate_persons_age(self) -> None:\n    from models.person import Person\n    for index, person_reference in enumerate(self.persons or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = await person_reference\n        else:\n            person = await Reference(**person_reference)\n        if person.age == 'N/A':\n            raise ValueError('Invalid DOB format. Please use YYYY-MM-DD')\n        if person.age < 18:\n            raise ValueError(f'{person.first_name} {person.last_name}: Age must be 18 or older')",
                "table_name": "Journey",
                "primary_key": ["partition_key"],
                "foreign_keys": {"country": [{"country_partition_key": "string"}, "Country", ["partition_key"]]},
            },
        ),
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="Person",
            old_schema={
                "title": "Person",
                "properties": {
                    "first_name": {"type": "string", "title": "first_name"},
                    "last_name": {"type": "string", "title": "last_name"},
                    "dob": {"type": "string", "title": "dob"},
                },
                "custom_code": "@property\ndef display_name(self) -> str:\n    from datetime import date, datetime\n    today = date.today()\n    try:\n        birthdate = datetime.strptime(self.dob, '%Y-%m-%d')\n    except (TypeError, ValueError):\n        age = 'N/A'\n    else:\n        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n    return f'{self.first_name} {self.last_name} ({age} years old)'",
                "table_name": "Person",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
            new_schema={
                "title": "Person",
                "properties": {
                    "first_name": {"type": "string", "title": "first_name"},
                    "last_name": {"type": "string", "title": "last_name"},
                    "dob": {"type": "string", "title": "dob"},
                },
                "custom_code": "@property\ndef age(self):\n    from datetime import date, datetime\n    today = date.today()\n    try:\n        birthdate = datetime.strptime(self.dob, '%Y-%m-%d')\n    except (TypeError, ValueError):\n        return 'N/A'\n    else:\n        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n\n@property\ndef display_name(self) -> str:\n    return f'{self.first_name} {self.last_name} ({self.age} years old)'",
                "table_name": "Person",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
        ),
    ]
