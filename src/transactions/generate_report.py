import base64

import jinja2
from datetime import datetime

from amsdal import Metadata
from amsdal import Versions
from amsdal import Reference
from amsdal.models import Model
from amsdal.transactions import async_transaction

from models.booking import Booking
from models.journey import Journey
from models.person import Person


@async_transaction
async def GenerateReport():
    upcoming_journey = await get_upcoming_journey()

    if not upcoming_journey:
        raise ValueError("No upcoming journey found")

    # Preload the m2m relationships
    await upcoming_journey.persons
    await upcoming_journey.bookings

    history_changes = await get_history_changes(upcoming_journey)
    html_buffer = await render_html(upcoming_journey, history_changes)

    # Send this HTML in E-mail, although we will just write to the file
    with open("report.html", "wt") as f:
        f.write(html_buffer)

    return {
        "html": html_buffer,
    }

async def get_upcoming_journey():
    qs = Journey.objects.filter(start_timestamp__gt=datetime.now().timestamp())
    qs = qs.order_by("start_timestamp")

    return await qs.first().aexecute()

async def get_history_changes(journey: Journey):
    history = []

    # get all history changes for the journey itself
    history.extend(await _get_history_changes_for_model(Journey, journey, "Journey"))

    # get all history changes for the bookings
    for booking in journey.bookings:
        history.extend(await _get_history_changes_for_model(Booking, booking, "Booking"))

    # get all history changes for the persons
    for person in journey.persons:
        history.extend(await _get_history_changes_for_model(Person, person, "Person"))

    # sort history by order_key
    history.sort(key=lambda x: x["order_key"])

    return history


async def _get_history_changes_for_model(model, obj: Model | Reference, model_name):
    history = []

    qs = model.objects.filter(
        _address__class_version=Versions.ALL,
        _address__object_id=obj.object_id if isinstance(obj, Model) else obj.ref.object_id,
        _address__object_version_id=Versions.ALL,
    )

    item: Model
    for item in await qs.aexecute():
        history.append(
            {
                "order_key": (await item.aget_metadata()).updated_at,
                "date": _ms_to_date((await item.aget_metadata()).updated_at),
                "model": model_name,
                "action": _resolve_action((await item.aget_metadata())),
                "display_name": getattr(
                    item, "display_name", str((await item.aget_metadata()).address)
                ),
            }
        )

    return history


def _ms_to_date(ms: int):
    return datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d")


def _resolve_action(metadata: Metadata):
    if metadata.is_deleted:
        return "Deleted"
    elif metadata.next_version:
        return "Changed"
    else:
        return "Created"

async def render_html(journey: Journey, history_changes: list):
    loader = jinja2.FileSystemLoader(searchpath="./static")
    env = jinja2.Environment(loader=loader, extensions=["jinja2.ext.loopcontrols"])

    def base64_encode(value):
        if not isinstance(value, bytes):
            raise TypeError("Input must be bytes")

        result = base64.b64encode(value).decode("utf-8")

        return f"data:image/jpeg;base64,{result}"

    env.filters["base64"] = base64_encode

    template = env.get_template("template.html")

    return template.render(
        journey=await journey.amodel_dump(),
        history_changes=history_changes,
    )