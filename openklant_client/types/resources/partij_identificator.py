from typing import Literal, NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import ForeignKeyRef, PaginationParams

#
# Input
#

CodeObjecttype = Literal[
    "natuurlijk_persoon",
    "niet_natuurlijk_persoon",
    "overig",
    "vestiging",
]

CodeSoortObjectId = Literal[
    "bsn",
    "kvk_nummer",
    "overig",
    "rsin",
    "vestigingsnummer",
]

CodeRegister = Literal[
    "brp",
    "hr",
    "overig",
]


class PartijIdentificatorObject(TypedDict):
    codeObjecttype: CodeObjecttype
    codeSoortObjectId: CodeSoortObjectId
    codeRegister: CodeRegister
    objectId: str


class CreateIdentificeerdePartij(TypedDict):
    uuid: str


# For use in the Partij creation endpoint
class CreateEmbeddedPartijIdentificatorData(TypedDict):
    partijIdentificator: PartijIdentificatorObject
    anderePartijIdentificator: NotRequired[str]
    subIdentificatorVan: NotRequired[ForeignKeyRef]


class CreatePartijIdentificatorData(TypedDict):
    identificeerdePartij: CreateIdentificeerdePartij
    partijIdentificator: PartijIdentificatorObject
    anderePartijIdentificator: NotRequired[str]
    subIdentificatorVan: NotRequired[ForeignKeyRef]


class ListPartijIdentificatorenParams(PaginationParams, total=False):
    partijIdentificatorCodeObjecttype: CodeObjecttype
    partijIdentificatorCodeRegister: CodeRegister
    partijIdentificatorCodeSoortObjectId: CodeSoortObjectId
    partijIdentificatorObjectId: str


#
# Output
#


class IdentificerendePartij(TypedDict):
    uuid: str
    url: str


class PartijIdentificator(TypedDict):
    uuid: str
    identificeerdePartij: IdentificerendePartij
    partijIdentificator: PartijIdentificatorObject
    anderePartijIdentificator: NotRequired[str]
    subIdentificatorVan: ForeignKeyRef | None
