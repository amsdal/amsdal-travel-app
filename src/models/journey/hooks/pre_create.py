from amsdal import Reference
from amsdal import ReferenceLoader


def pre_create(self) -> None:
    self.validate_persons_age()


def validate_persons_age(self) -> None:
    from models.person import Person

    for index, person_reference in enumerate(self.persons or []):
        person: Person
        if isinstance(person_reference, Person):
            person = person_reference
        elif isinstance(person_reference, Reference):
            person = ReferenceLoader(person_reference).load_reference()
        else:
            person = ReferenceLoader(Reference(**person_reference)).load_reference()

        if person.age == "N/A":
            raise ValueError("Invalid DOB format. Please use YYYY-MM-DD")

        if person.age < 18:
            raise ValueError(
                f"{person.first_name} {person.last_name}: Age must be 18 or older"
            )