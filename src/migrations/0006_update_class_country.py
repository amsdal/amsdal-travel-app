from amsdal_models.migration import migrations
from amsdal_utils.models.enums import ModuleType


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="Country",
            old_schema={
                "title": "Country",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "code": {"type": "string", "title": "code"},
                },
                "custom_code": "@property\ndef display_name(self) -> str:\n    return self.name",
                "table_name": "Country",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
            new_schema={
                "title": "Country",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "code": {"type": "string", "title": "code"},
                },
                "custom_code": "@property\ndef display_name(self) -> str:\n    return self.name",
                "storage_metadata": {
                    "table_name": "Country",
                    "db_fields": {},
                    "primary_key": ["partition_key"],
                    "foreign_keys": {},
                },
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
                "custom_code": "@property\ndef age(self):\n    from datetime import date\n    from datetime import datetime\n    today = date.today()\n    try:\n        birthdate = datetime.strptime(self.dob, '%Y-%m-%d')\n    except (TypeError, ValueError):\n        return 'N/A'\n    else:\n        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n\n@property\ndef display_name(self) -> str:\n    return f'{self.first_name} {self.last_name} ({self.age} years old)'",
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
                "custom_code": "@property\ndef age(self):\n    from datetime import date\n    from datetime import datetime\n    today = date.today()\n    try:\n        birthdate = datetime.strptime(self.dob, '%Y-%m-%d')\n    except (TypeError, ValueError):\n        return 'N/A'\n    else:\n        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n\n@property\ndef display_name(self) -> str:\n    return f'{self.first_name} {self.last_name} ({self.age} years old)'",
                "storage_metadata": {
                    "table_name": "Person",
                    "db_fields": {},
                    "primary_key": ["partition_key"],
                    "foreign_keys": {},
                },
            },
        ),
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="Property",
            old_schema={
                "title": "Property",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "type": {"type": "string", "title": "type"},
                    "address": {"type": "string", "title": "address"},
                    "free_parking": {"type": "boolean", "title": "free_parking"},
                    "free_wifi": {"type": "boolean", "title": "free_wifi"},
                    "photos": {"type": "array", "items": {"type": "File"}, "title": "photos"},
                },
                "custom_code": "from amsdal.models.core.file import *",
                "table_name": "Property",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
            new_schema={
                "title": "Property",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "type": {"type": "string", "title": "type"},
                    "address": {"type": "string", "title": "address"},
                    "free_parking": {"type": "boolean", "title": "free_parking"},
                    "free_wifi": {"type": "boolean", "title": "free_wifi"},
                    "photos": {"type": "array", "items": {"type": "File"}, "title": "photos"},
                },
                "custom_code": "from amsdal.models.core.file import *",
                "storage_metadata": {
                    "table_name": "Property",
                    "db_fields": {},
                    "primary_key": ["partition_key"],
                    "foreign_keys": {},
                },
            },
        ),
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="Journey",
            old_schema={
                "title": "Journey",
                "properties": {
                    "start_date": {"type": "string", "title": "start_date"},
                    "start_timestamp": {"type": "number", "title": "start_timestamp"},
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
                "custom_code": "from typing import Any\n\nfrom amsdal import Reference\nfrom amsdal_models.builder.validators.dict_validators import validate_non_empty_keys\nfrom pydantic.functional_validators import field_validator\n\nfrom models.booking import *\nfrom models.country import *\nfrom models.person import *\n\n\n@field_validator('equipment')\n@classmethod\ndef _non_empty_keys_equipment(cls: type, value: Any) -> Any:\n    return validate_non_empty_keys(value)\n\nasync def apre_create(self) -> None:\n    await self.validate_persons_age()\n\nasync def validate_persons_age(self) -> None:\n    from models.person import Person\n    for index, person_reference in enumerate(self.persons or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = await person_reference\n        else:\n            person = await Reference(**person_reference)\n        if person.age == 'N/A':\n            raise ValueError('Invalid DOB format. Please use YYYY-MM-DD')\n        if person.age < 18:\n            raise ValueError(f'{person.first_name} {person.last_name}: Age must be 18 or older')\n\ndef post_init(self, is_new_object, kwargs):\n    from datetime import datetime\n    try:\n        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')\n    except (TypeError, ValueError):\n        self.start_timestamp = None\n    else:\n        self.start_timestamp = start_date.timestamp()",
                "table_name": "Journey",
                "primary_key": ["partition_key"],
                "foreign_keys": {"country": [{"country_partition_key": "string"}, "Country", ["partition_key"]]},
            },
            new_schema={
                "title": "Journey",
                "properties": {
                    "start_date": {"type": "string", "title": "start_date"},
                    "start_timestamp": {"type": "number", "title": "start_timestamp"},
                    "end_date": {"type": "string", "title": "end_date"},
                    "country": {"type": "Country", "title": "country"},
                    "equipment": {
                        "type": "dictionary",
                        "items": {"key": {"type": "string"}, "value": {"type": "number"}},
                        "title": "equipment",
                    },
                    "persons": {"type": "array", "items": {"type": "Person"}, "title": "persons"},
                    "bookings": {"type": "array", "items": {"type": "Booking"}, "title": "bookings"},
                },
                "custom_code": "from typing import Any\n\nfrom amsdal import Reference\nfrom amsdal_models.builder.validators.dict_validators import validate_non_empty_keys\nfrom pydantic.functional_validators import field_validator\n\nfrom models.booking import *\nfrom models.country import *\nfrom models.person import *\n\n\n@field_validator('equipment')\n@classmethod\ndef _non_empty_keys_equipment(cls: type, value: Any) -> Any:\n    return validate_non_empty_keys(value)\n\nasync def apre_create(self) -> None:\n    await self.validate_persons_age()\n\nasync def validate_persons_age(self) -> None:\n    from models.person import Person\n    for index, person_reference in enumerate(self.persons or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = await person_reference\n        else:\n            person = await Reference(**person_reference)\n        if person.age == 'N/A':\n            raise ValueError('Invalid DOB format. Please use YYYY-MM-DD')\n        if person.age < 18:\n            raise ValueError(f'{person.first_name} {person.last_name}: Age must be 18 or older')\n\ndef post_init(self, is_new_object, kwargs):\n    from datetime import datetime\n    try:\n        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')\n    except (TypeError, ValueError):\n        self.start_timestamp = None\n    else:\n        self.start_timestamp = start_date.timestamp()",
                "storage_metadata": {
                    "table_name": "Journey",
                    "db_fields": {"country": ["country_partition_key"]},
                    "primary_key": ["partition_key"],
                    "foreign_keys": {"country": [{"country_partition_key": "string"}, "Country", ["partition_key"]]},
                },
            },
        ),
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="Booking",
            old_schema={
                "title": "Booking",
                "properties": {
                    "property": {"type": "Property", "title": "property", "db_field": ["property_partition_key"]},
                    "date": {"type": "string", "title": "date"},
                    "nights": {"type": "number", "default": 1.0, "title": "nights"},
                },
                "custom_code": "from models.property import *",
                "table_name": "Booking",
                "primary_key": ["partition_key"],
                "foreign_keys": {"property": [{"property_partition_key": "string"}, "Property", ["partition_key"]]},
            },
            new_schema={
                "title": "Booking",
                "properties": {
                    "property": {"type": "Property", "title": "property"},
                    "date": {"type": "string", "title": "date"},
                    "nights": {"type": "number", "default": 1.0, "title": "nights"},
                },
                "custom_code": "from models.property import *",
                "storage_metadata": {
                    "table_name": "Booking",
                    "db_fields": {"property": ["property_partition_key"]},
                    "primary_key": ["partition_key"],
                    "foreign_keys": {"property": [{"property_partition_key": "string"}, "Property", ["partition_key"]]},
                },
            },
        ),
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="PropertyFile",
            old_schema={
                "title": "PropertyFile",
                "required": ["property", "file"],
                "properties": {
                    "property": {"type": "Property", "title": "Property", "db_field": ["property_partition_key"]},
                    "file": {"type": "File", "title": "File", "db_field": ["file_partition_key"]},
                },
                "table_name": "PropertyFile",
                "primary_key": ["property", "file"],
                "foreign_keys": {
                    "property": [{"property_partition_key": "string"}, "Property", ["partition_key"]],
                    "file": [{"file_partition_key": "string"}, "File", ["partition_key"]],
                },
            },
            new_schema={
                "title": "PropertyFile",
                "required": ["property", "file"],
                "properties": {
                    "property": {"type": "Property", "title": "Property"},
                    "file": {"type": "File", "title": "File"},
                },
                "storage_metadata": {
                    "table_name": "PropertyFile",
                    "db_fields": {"property": ["property_partition_key"], "file": ["file_partition_key"]},
                    "primary_key": ["property", "file"],
                    "foreign_keys": {
                        "property": [{"property_partition_key": "string"}, "Property", ["partition_key"]],
                        "file": [{"file_partition_key": "string"}, "File", ["partition_key"]],
                    },
                },
            },
        ),
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="JourneyPerson",
            old_schema={
                "title": "JourneyPerson",
                "required": ["journey", "person"],
                "properties": {
                    "journey": {"type": "Journey", "title": "Journey", "db_field": ["journey_partition_key"]},
                    "person": {"type": "Person", "title": "Person", "db_field": ["person_partition_key"]},
                },
                "table_name": "JourneyPerson",
                "primary_key": ["journey", "person"],
                "foreign_keys": {
                    "journey": [{"journey_partition_key": "string"}, "Journey", ["partition_key"]],
                    "person": [{"person_partition_key": "string"}, "Person", ["partition_key"]],
                },
            },
            new_schema={
                "title": "JourneyPerson",
                "required": ["journey", "person"],
                "properties": {
                    "journey": {"type": "Journey", "title": "Journey"},
                    "person": {"type": "Person", "title": "Person"},
                },
                "storage_metadata": {
                    "table_name": "JourneyPerson",
                    "db_fields": {"journey": ["journey_partition_key"], "person": ["person_partition_key"]},
                    "primary_key": ["journey", "person"],
                    "foreign_keys": {
                        "journey": [{"journey_partition_key": "string"}, "Journey", ["partition_key"]],
                        "person": [{"person_partition_key": "string"}, "Person", ["partition_key"]],
                    },
                },
            },
        ),
        migrations.UpdateClass(
            module_type=ModuleType.USER,
            class_name="JourneyBooking",
            old_schema={
                "title": "JourneyBooking",
                "required": ["journey", "booking"],
                "properties": {
                    "journey": {"type": "Journey", "title": "Journey", "db_field": ["journey_partition_key"]},
                    "booking": {"type": "Booking", "title": "Booking", "db_field": ["booking_partition_key"]},
                },
                "table_name": "JourneyBooking",
                "primary_key": ["journey", "booking"],
                "foreign_keys": {
                    "journey": [{"journey_partition_key": "string"}, "Journey", ["partition_key"]],
                    "booking": [{"booking_partition_key": "string"}, "Booking", ["partition_key"]],
                },
            },
            new_schema={
                "title": "JourneyBooking",
                "required": ["journey", "booking"],
                "properties": {
                    "journey": {"type": "Journey", "title": "Journey"},
                    "booking": {"type": "Booking", "title": "Booking"},
                },
                "storage_metadata": {
                    "table_name": "JourneyBooking",
                    "db_fields": {"journey": ["journey_partition_key"], "booking": ["booking_partition_key"]},
                    "primary_key": ["journey", "booking"],
                    "foreign_keys": {
                        "journey": [{"journey_partition_key": "string"}, "Journey", ["partition_key"]],
                        "booking": [{"booking_partition_key": "string"}, "Booking", ["partition_key"]],
                    },
                },
            },
        ),
    ]
