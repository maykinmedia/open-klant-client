from typing import Literal, NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import (
    Adres,
    ForeignKeyRef,
    FullForeigKeyRef,
    PaginationParams,
)

BetrokkeneRol = Literal["vertegenwoordiger", "klant"]


class CreateContactnaam(TypedDict):
    voorletters: NotRequired[str]
    voornaam: str
    voorvoegselAchternaam: NotRequired[str]
    achternaam: str


class BetrokkeneBaseCreateData(TypedDict):
    wasPartij: NotRequired[ForeignKeyRef | None]
    bezoekadres: NotRequired[Adres]
    correspondentieadres: NotRequired[Adres]
    contactnaam: NotRequired[CreateContactnaam | None]
    rol: BetrokkeneRol
    organisatienaam: str
    initiator: bool


class BetrokkeneCreateData(BetrokkeneBaseCreateData):
    hadKlantcontact: ForeignKeyRef


class Betrokkene(TypedDict):
    uuid: str
    url: str
    wasPartij: FullForeigKeyRef | None
    hadKlantcontact: FullForeigKeyRef
    digitaleAdressen: list[FullForeigKeyRef]
    bezoekadres: Adres
    correspondentieadres: Adres
    contactnaam: CreateContactnaam
    volledigeNaam: str
    rol: BetrokkeneRol
    organisatienaam: str
    initiator: bool


class BetrokkeneRetrieveParams(TypedDict):
    expand: NotRequired[list[Literal["digitaleAdressen",]]]


class BetrokkeneListParams(PaginationParams, total=False):
    contactnaamAchternaam: str
    contactnaamVoorletters: str
    contactnaamVoornaam: str
    contactnaamVoorvoegselAchternaam: str
    expand: list[Literal["digitaleAdressen"]]
    hadKlantcontact__referentienummer: str
    hadKlantcontact__url: str
    hadKlantcontact__uuid: str
    organisatienaam: str
    verstrektedigitaalAdres__adres: str
    verstrektedigitaalAdres__url: str
    verstrektedigitaalAdres__uuid: str
    wasPartij__partijIdentificator__codeObjecttype: str
    wasPartij__partijIdentificator__codeRegister: str
    wasPartij__partijIdentificator__codeSoortObjectId: str
    wasPartij__partijIdentificator__objectId: str
    wasPartij__url: str
    wasPartij__uuid: str
