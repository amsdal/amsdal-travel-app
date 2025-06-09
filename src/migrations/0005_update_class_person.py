from amsdal_models.migration import migrations
from amsdal_utils.models.enums import ModuleType


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
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
                "custom_code": "@property\ndef age(self):\n    from datetime import date, datetime\n    today = date.today()\n    try:\n        birthdate = datetime.strptime(self.dob, '%Y-%m-%d')\n    except (TypeError, ValueError):\n        return 'N/A'\n    else:\n        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n\n@property\ndef display_name(self) -> str:\n    return f'{self.first_name} {self.last_name} ({self.age} years old)'",
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
                "table_name": "Person",
                "primary_key": ["partition_key"],
                "foreign_keys": {},
            },
        ),
    ]
