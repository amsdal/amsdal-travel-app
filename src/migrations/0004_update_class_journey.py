from amsdal.migration import migrations
from amsdal_utils.models.enums import SchemaTypes


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
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
                "custom_code": 'from amsdal_utils.models.data_models.reference import Reference\nfrom amsdal_models.classes.helpers.reference_loader import ReferenceLoader\n\n\ndef pre_init(self, is_new_object, kwargs):\n    if not is_new_object:\n        # This is an update, not create, so skip age checking\n        return\n\n    self.validate_persons_age(kwargs)\n\n\ndef validate_persons_age(self, data):\n    from models.user.person import Person\n\n    for index, person_reference in enumerate(data.get("persons") or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = ReferenceLoader(person_reference).load_reference()\n        else:\n            person = ReferenceLoader(Reference(**person_reference)).load_reference()\n\n        if person.age == "N/A":\n            raise ValueError("Invalid DOB format. Please use YYYY-MM-DD")\n\n        if person.age < 18:\n            raise ValueError(\n                f"{person.first_name} {person.last_name}: Age must be 18 or older"\n            )',
                "indexed": [],
            },
            new_schema={
                "title": "Journey",
                "properties": {
                    "start_date": {"type": "string", "title": "start_date"},
                    "start_timestamp": {"type": "number", "title": "start_timestamp"},
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
                "custom_code": 'def post_init(self, is_new_object, kwargs):\n    from datetime import datetime\n\n    try:\n        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")\n    except (TypeError, ValueError):\n        self.start_timestamp = None\n    else:\n        self.start_timestamp = start_date.timestamp()\n\nfrom amsdal_utils.models.data_models.reference import Reference\nfrom amsdal_models.classes.helpers.reference_loader import ReferenceLoader\n\n\ndef pre_init(self, is_new_object, kwargs):\n    if not is_new_object:\n        # This is an update, not create, so skip age checking\n        return\n\n    self.validate_persons_age(kwargs)\n\n\ndef validate_persons_age(self, data):\n    from models.user.person import Person\n\n    for index, person_reference in enumerate(data.get("persons") or []):\n        person: Person\n        if isinstance(person_reference, Person):\n            person = person_reference\n        elif isinstance(person_reference, Reference):\n            person = ReferenceLoader(person_reference).load_reference()\n        else:\n            person = ReferenceLoader(Reference(**person_reference)).load_reference()\n\n        if person.age == "N/A":\n            raise ValueError("Invalid DOB format. Please use YYYY-MM-DD")\n\n        if person.age < 18:\n            raise ValueError(\n                f"{person.first_name} {person.last_name}: Age must be 18 or older"\n            )',
                "indexed": [],
            },
        ),
    ]
