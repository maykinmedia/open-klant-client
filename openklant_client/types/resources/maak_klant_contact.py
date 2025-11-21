from typing import NotRequired, TypedDict

from .betrokkene import Betrokkene, BetrokkeneBaseCreateData
from .klant_contact import CreateKlantContactData, KlantContact
from .onderwerp_object import OnderwerpObject, OnderwerpObjectBaseCreateData


class MaakKlantContactCreateData(TypedDict):
    klantcontact: CreateKlantContactData
    betrokkene: NotRequired[BetrokkeneBaseCreateData]
    onderwerpobject: NotRequired[OnderwerpObjectBaseCreateData]


class MaakKlantContact(TypedDict):
    klantcontact: KlantContact
    betrokkene: Betrokkene | None
    onderwerpobject: OnderwerpObject | None
