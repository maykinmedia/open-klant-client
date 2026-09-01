from typing import Literal, NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import (
    ForeignKeyRef,
    FullForeigKeyRef,
    PaginationParams,
)


class CreateInterneTaakData(TypedDict):
    nummer: NotRequired[str]
    gevraagdeHandeling: str
    aanleidinggevendKlantcontact: ForeignKeyRef
    toegewezenAanActor: ForeignKeyRef
    toelichting: NotRequired[str]
    status: Literal["te_verwerken", "verwerkt"]


class InterneTaakListParams(PaginationParams, total=False):
    aanleidinggevendKlantcontact__url: str
    aanleidinggevendKlantcontact__uuid: str
    actoren__naam: str
    klantcontact__referentienummer: str
    klantcontact__uuid: str
    referentienummer: str
    status: Literal["te_verwerken", "verwerkt"]
    toegewezenAanActor__url: str
    toegewezenAanActor__uuid: str
    toegewezenOp: str


class InterneTaak(TypedDict):
    uuid: str
    url: str
    nummer: str | None
    gevraagdeHandeling: str
    aanleidinggevendKlantcontact: FullForeigKeyRef
    toegewezenAanActor: FullForeigKeyRef
    toelichting: str
    status: Literal["te_verwerken", "verwerkt"]
    toegewezenOp: str
    afgehandeldOp: str | None
