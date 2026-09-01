import uuid
from typing import cast

from ape_pie import APIClient

from openklant_client._resources.base import ResourceMixin
from openklant_client.types.pagination import PaginatedResponseBody
from openklant_client.types.resources.partij import (
    CreatePartijContactpersoonData,
    CreatePartijOrganisatieData,
    CreatePartijPersoonData,
    PartialUpdatePartijData,
    Partij,
    PartijListParams,
    PartijRetrieveParams,
)


class PartijResource(ResourceMixin):
    http_client: APIClient
    base_path: str = "partijen"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_iter = self._make_list_iter(self.list)

    def list(
        self, *, params: PartijListParams | None = None
    ) -> PaginatedResponseBody[Partij]:
        response = self._get(self.base_path, params=params)
        return cast(PaginatedResponseBody[Partij], self.process_response(response))

    def retrieve(
        self, /, uuid: str | uuid.UUID, *, params: PartijRetrieveParams | None = None
    ) -> Partij:
        response = self._get(f"{self.base_path}/{uuid!s}", params=params)
        return cast(Partij, self.process_response(response))

    # Partij is polymorphic on "soortPartij", with varying fields for
    # Persoon, Organisatie and ContactPersoon
    def create_organisatie(self, *, data: CreatePartijOrganisatieData) -> Partij:
        return self._create(data=data)

    def create_persoon(
        self,
        *,
        data: CreatePartijPersoonData,
    ) -> Partij:
        return cast(Partij, self._create(data=data))

    def create_contactpersoon(
        self,
        *,
        data: CreatePartijContactpersoonData,
    ) -> Partij:
        return cast(Partij, self._create(data=data))

    def _create(
        self,
        *,
        data: (
            CreatePartijPersoonData
            | CreatePartijOrganisatieData
            | CreatePartijContactpersoonData
        ),
    ) -> Partij:
        response = self._post(self.base_path, data=data)
        return cast(Partij, self.process_response(response))

    def partial_update(
        self, /, uuid: str | uuid.UUID, *, data: PartialUpdatePartijData
    ) -> Partij:
        response = self._patch(f"{self.base_path}/{uuid!s}", data=data)
        return cast(Partij, self.process_response(response))
