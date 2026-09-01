from typing import Literal, NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import (
    ForeignKeyRef,
    FullForeigKeyRef,
    PaginationParams,
)

SoortDigitaalAdres = Literal["email", "telefoonnummer", "overig"]


#
# Input
#


class DigitaalAdresCreateData(TypedDict):
    verstrektDoorBetrokkene: ForeignKeyRef | None
    verstrektDoorPartij: ForeignKeyRef | None
    adres: str
    omschrijving: str
    soortDigitaalAdres: SoortDigitaalAdres
    isStandaardAdres: NotRequired[bool]
    referentie: NotRequired[str]


class DigitaalAdresPartialUpdateData(TypedDict):
    verstrektDoorBetrokkene: NotRequired[ForeignKeyRef | None]
    verstrektDoorPartij: NotRequired[ForeignKeyRef | None]
    adres: NotRequired[str]
    omschrijving: NotRequired[str]
    soortDigitaalAdres: NotRequired[SoortDigitaalAdres]
    isStandaardAdres: NotRequired[bool]
    referentie: NotRequired[str]


class ListDigitaalAdresParams(PaginationParams):
    verstrektDoorPartij__uuid: NotRequired[str]
    verstrektDoorPartij__partijIdentificator__codeObjecttype: NotRequired[str]
    verstrektDoorPartij__partijIdentificator__codeRegister: NotRequired[str]
    verstrektDoorPartij__partijIdentificator__codeSoortObjectId: NotRequired[str]
    verstrektDoorPartij__partijIdentificator__objectId: NotRequired[str]
    verstrektDoorPartij__soortPartij: NotRequired[
        Literal["organisatie", "persoon", "contactpersoon"]
    ]
    verstrektDoorBetrokkene__uuid: NotRequired[str]
    adres: NotRequired[str]
    soortDigitaalAdres: NotRequired[SoortDigitaalAdres]
    referentie: NotRequired[str]


#
# Output
#


class DigitaalAdres(TypedDict):
    uuid: str
    url: str
    verstrektDoorBetrokkene: FullForeigKeyRef | None
    verstrektDoorPartij: FullForeigKeyRef | None
    adres: str
    omschrijving: str
    soortDigitaalAdres: SoortDigitaalAdres
    isStandaardAdres: bool
    referentie: str
