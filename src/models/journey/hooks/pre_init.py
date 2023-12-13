from amsdal_models.errors import AmsdalValidationError
from amsdal_utils.models.data_models.reference import Reference
from amsdal_models.classes.helpers.reference_loader import ReferenceLoader


def pre_init(self, is_new_object, kwargs):
    if not is_new_object:
        # This is an update, not create, so skip age checking
        return

    self.validate_persons_age(kwargs)


def validate_persons_age(self, data):
    from models.user.person import Person

    for index, person_reference in enumerate(data.get("persons") or []):
        person: Person
        if isinstance(person_reference, Person):
            person = person_reference
        elif isinstance(person_reference, Reference):
            person = ReferenceLoader(person_reference).load_reference()
        else:
            person = ReferenceLoader(Reference(**person_reference)).load_reference()

        if person.age == "N/A":
            raise AmsdalValidationError("Invalid DOB format. Please use YYYY-MM-DD")

        if person.age < 18:
            raise AmsdalValidationError(
                f"{person.first_name} {person.last_name}: Age must be 18 or older"
            )
