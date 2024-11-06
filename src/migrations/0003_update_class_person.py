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
                "custom_code": '@property\ndef display_name(self) -> str:\n    from datetime import datetime\n    from datetime import date\n\n    today = date.today()\n\n    try:\n        birthdate = datetime.strptime(self.dob, "%Y-%m-%d")\n    except (TypeError, ValueError):\n        age = "N/A"\n    else:\n        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n\n    return f"{self.first_name} {self.last_name} ({age} years old)"',
                "indexed": [],
            },
            new_schema={
                "title": "Person",
                "properties": {
                    "first_name": {"type": "string", "title": "first_name"},
                    "last_name": {"type": "string", "title": "last_name"},
                    "dob": {"type": "string", "title": "dob"},
                },
                "custom_code": '@property\ndef display_name(self) -> str:\n    return f"{self.first_name} {self.last_name} ({self.age} years old)"\n\n@property\ndef age(self):\n    from datetime import datetime\n    from datetime import date\n\n    today = date.today()\n\n    try:\n        birthdate = datetime.strptime(self.dob, "%Y-%m-%d")\n    except (TypeError, ValueError):\n        return "N/A"\n    else:\n        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))',
                "indexed": [],
            },
        ),
        migrations.UpdateClass(
            schema_type=SchemaTypes.USER,
            class_name="Journey",
            old_schema={
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
                "custom_code": 'from datetime import datetime\nfrom datetime import date\nfrom amsdal_utils.models.data_models.reference import Reference\nfrom amsdal_models.classes.helpers.reference_loader import ReferenceLoader\n\n\ndef pre_init(self, is_new_object, kwargs):\n    if not is_new_object:\n        # This is an update, not create, so skip age checking\n        return\n\n    self.validate_persons_age(kwargs)\n\n\ndef validate_persons_age(self, data):\n    from models.user.person import Person\n\n    for index, person_reference in enumerate(data.get("persons") or []):\n        person: Person\n\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = ReferenceLoader(person_reference).load_reference()\n        else:\n            person = ReferenceLoader(Reference(**person_reference)).load_reference()\n\n        try:\n            birthdate = datetime.strptime(person.dob, "%Y-%m-%d")\n        except (TypeError, ValueError):\n            continue\n\n        today = date.today()\n        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))\n\n        if age < 18:\n            raise ValueError(f"{person.first_name} {person.last_name}: Age must be 18 or older")',
                "indexed": [],
            },
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
                "custom_code": 'from amsdal_utils.models.data_models.reference import Reference\nfrom amsdal_models.classes.helpers.reference_loader import ReferenceLoader\n\n\ndef pre_init(self, is_new_object, kwargs):\n    if not is_new_object:\n        # This is an update, not create, so skip age checking\n        return\n\n    self.validate_persons_age(kwargs)\n\n\ndef validate_persons_age(self, data):\n    from models.user.person import Person\n\n    for index, person_reference in enumerate(data.get("persons") or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = ReferenceLoader(person_reference).load_reference()\n        else:\n            person = ReferenceLoader(Reference(**person_reference)).load_reference()\n\n        if person.age == "N/A":\n            raise ValueError("Invalid DOB format. Please use YYYY-MM-DD")\n\n        if person.age < 18:\n            raise ValueError(\n                f"{person.first_name} {person.last_name}: Age must be 18 or older"\n            )',
                "indexed": [],
            },
        ),
    ]
