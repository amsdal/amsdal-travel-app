import random
from datetime import date, timedelta
from datetime import datetime

from amsdal_data.transactions import transaction
from amsdal_models.errors import AmsdalValidationError
from models.user.booking import Booking
from models.user.country import Country
from models.user.journey import Journey
from models.user.person import Person
from models.user.property import Property


@transaction
def BuildJourney(
    countries: list[Country],
    nights: int,
    total_nights: int,
    persons: list[Person],
    equipment: dict[str, int],
):
    country = get_country_by_trend(countries)
    start_date = get_best_start_date(country)
    bookings = book_best_properties(country, start_date, nights, total_nights)
    last_booking = bookings[-1]
    end_date = datetime.strptime(last_booking.date, "%Y-%m-%d") + timedelta(
        days=last_booking.nights
    )
    journey_start_date = start_date.strftime("%Y-%m-%d")
    journey_end_date = end_date.strftime("%Y-%m-%d")

    journey = Journey(
        start_date=journey_start_date,
        end_date=journey_end_date,
        country=country,
        persons=persons,
        equipment=equipment,
        bookings=bookings,
    )
    journey.save()

    return {
        "start_date": journey.start_date,
    }


def get_country_by_trend(countries: list[Country]) -> Country:
    if len(countries) == 0:
        raise AmsdalValidationError("No countries specified")

    # TODO: get the most trending country for the current year
    return random.choice(countries)


def get_best_start_date(country: Country) -> date:
    # TODO: here we can check a weather forecast for the country and find the best closest start date
    return date.today() + timedelta(days=random.randint(30, 45))


def book_best_properties(
    country: Country, start_date: date, nights: int, total_nights: int
):
    # TODO: here we can use external API to find the best properties for the country and book the available ones
    bookings = []
    properties = Property.objects.all().execute()
    rest_nights = total_nights

    if len(properties) == 0:
        raise AmsdalValidationError(
            f"No properties found for the country: {country.name}"
        )

    while len(properties) > 0 and rest_nights > 0:
        _property = random.choice(properties)
        properties.remove(_property)

        if not len(properties) or rest_nights <= 2 * nights:
            book_nights = rest_nights
            rest_nights = 0
        else:
            book_nights = nights
            rest_nights -= nights

        booking = Booking(
            property=_property,
            date=start_date.strftime("%Y-%m-%d"),
            nights=book_nights,
        )
        bookings.append(booking)

    return bookings
