from amsdal.migration import migrations
from amsdal_utils.models.enums import SchemaTypes


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.UpdateClass(
            schema_type=SchemaTypes.USER,
            class_name="Person",
            old_schema={
                "title": "Person",
                "properties": {
                    "first_name": {"type": "string", "title": "first_name"},
                    "last_name": {"type": "string", "title": "last_name"},
                    "dob": {"type": "string", "title": "dob"},
                },
                "indexed": [],
            },
            new_schema={
                "title": "Person",
                "properties": {
                    "first_name": {"type": "string", "title": "first_name"},
                    "last_name": {"type": "string", "title": "last_name"},
                    "dob": {"type": "string", "title": "dob"},
                },
                "custom_code": '@property\ndef display_name(self) -> str:\n    from datetime import datetime\n    from datetime import date\n\n    today = date.today()\n\n    try:\n        birthdate = datetime.strptime(self.dob, "%Y-%m-%d")\n    except (TypeError, ValueError):\n        age = "N/A"\n    else:\n        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n\n    return f"{self.first_name} {self.last_name} ({age} years old)"',
                "indexed": [],
            },
        ),
        migrations.UpdateClass(
            schema_type=SchemaTypes.USER,
            class_name="Country",
            old_schema={
                "title": "Country",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "code": {"type": "string", "title": "code"},
                },
                "indexed": [],
            },
            new_schema={
                "title": "Country",
                "properties": {
                    "name": {"type": "string", "title": "name"},
                    "code": {"type": "string", "title": "code"},
                },
                "custom_code": "@property\ndef display_name(self) -> str:\n    return self.name",
                "indexed": [],
            },
        ),
    ]
