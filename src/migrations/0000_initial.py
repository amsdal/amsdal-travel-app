from amsdal_models.migration import migrations
from amsdal_utils.models.enums import ModuleType


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="Property",
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
                "table_name": "Property",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
        ),
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="Country",
            new_schema={
                "title": "Country",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "code": {"type": "string", "title": "code"},
                },
                "table_name": "Country",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
        ),
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="PropertyFile",
            new_schema={
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
        ),
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="Booking",
            new_schema={
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
        ),
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="Journey",
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
                "custom_code": "from typing import Any\n\nfrom amsdal_models.builder.validators.dict_validators import validate_non_empty_keys\nfrom pydantic.functional_validators import field_validator\n\nfrom models.booking import *\nfrom models.country import *\nfrom models.person import *\n\n\n@field_validator('equipment')\n@classmethod\ndef _non_empty_keys_equipment(cls: type, value: Any) -> Any:\n    return validate_non_empty_keys(value)",
                "table_name": "Journey",
                "primary_key": ["partition_key"],
                "foreign_keys": {"country": [{"country_partition_key": "string"}, "Country", ["partition_key"]]},
            },
        ),
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="Person",
            new_schema={
                "title": "Person",
                "properties": {
                    "first_name": {"type": "string", "title": "first_name"},
                    "last_name": {"type": "string", "title": "last_name"},
                    "dob": {"type": "string", "title": "dob"},
                },
                "table_name": "Person",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
        ),
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="JourneyPerson",
            new_schema={
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
        ),
        migrations.CreateClass(
            module_type=ModuleType.USER,
            class_name="JourneyBooking",
            new_schema={
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
        ),
    ]
