from typing import cast

from ape_pie import APIClient

from openklant_client._resources.base import ResourceMixin
from openklant_client.types.resources.maak_klant_contact import (
    MaakKlantContact,
    MaakKlantContactCreateData,
)


class MaakKlantContactResource(ResourceMixin):
    http_client: APIClient
    base_path: str = "maak-klantcontact"
    """
    convenience endpoint to create of KlantContact, Betrokkene and OnderwerpObject
    """

    def create(
        self,
        *,
        data: MaakKlantContactCreateData,
    ) -> MaakKlantContact:
        response = self._post(self.base_path, data=data)
        return cast(MaakKlantContact, self.process_response(response))
