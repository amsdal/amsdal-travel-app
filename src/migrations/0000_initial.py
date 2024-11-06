from amsdal.migration import migrations
from amsdal_utils.models.enums import SchemaTypes


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.CreateClass(
            schema_type=SchemaTypes.USER,
            class_name="Person",
            new_schema={
                "title": "Person",
                "properties": {
                    "first_name": {"type": "string", "title": "first_name"},
                    "last_name": {"type": "string", "title": "last_name"},
                    "dob": {"type": "string", "title": "dob"},
                },
                "indexed": [],
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.USER,
            class_name="Journey",
            new_schema={
                "title": "Journey",
                "properties": {
                    "start_date": {"type": "string", "title": "start_date"},
                    "end_date": {"type": "string", "title": "end_date"},
                    "country": {"type": "Country", "title": "country"},
                    "persons": {"type": "array", "items": {"type": "Person"}, "title": "persons"},
                    "equipment": {
                        "type": "dictionary",
                        "items": {"key": {"type": "string"}, "value": {"type": "number"}},
                        "title": "equipment",
                    },
                    "bookings": {"type": "array", "items": {"type": "Booking"}, "title": "bookings"},
                },
                "indexed": [],
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.USER,
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
                "indexed": [],
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.USER,
            class_name="Country",
            new_schema={
                "title": "Country",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "code": {"type": "string", "title": "code"},
                },
                "indexed": [],
            },
        ),
        migrations.CreateClass(
            schema_type=SchemaTypes.USER,
            class_name="Booking",
            new_schema={
                "title": "Booking",
                "properties": {
                    "property": {"type": "Property", "title": "property"},
                    "date": {"type": "string", "title": "date"},
                    "nights": {"type": "number", "default": 1.0, "title": "nights"},
                },
                "indexed": [],
            },
        ),
    ]
