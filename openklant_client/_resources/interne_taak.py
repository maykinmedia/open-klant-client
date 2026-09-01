import uuid
from typing import cast

from ape_pie import APIClient

from openklant_client._resources.base import ResourceMixin
from openklant_client.types.pagination import PaginatedResponseBody
from openklant_client.types.resources.interne_taak import (
    CreateInterneTaakData,
    InterneTaak,
    InterneTaakListParams,
)


class InterneTaakResource(ResourceMixin):
    http_client: APIClient
    base_path: str = "internetaken"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_iter = self._make_list_iter(self.list)

    def create(
        self,
        *,
        data: CreateInterneTaakData,
    ) -> InterneTaak:
        response = self._post(self.base_path, data=data)
        return cast(InterneTaak, self.process_response(response))

    def retrieve(self, /, uuid: str | uuid.UUID) -> InterneTaak:
        response = self._get(f"{self.base_path}/{uuid!s}")
        return cast(InterneTaak, self.process_response(response))

    def list(
        self, *, params: InterneTaakListParams | None = None
    ) -> PaginatedResponseBody[InterneTaak]:
        response = self._get(f"{self.base_path}", params=params)
        return cast(
            PaginatedResponseBody[InterneTaak],
            self.process_response(response),
        )
