import pytest
from pydantic import TypeAdapter

from openklant_client.types.pagination import PaginatedResponseBody
from openklant_client.types.resources import Partij
from openklant_client.types.resources.digitaal_adres import (
    DigitaalAdres,
)
from tests.factories.digitaal_adres import DigitaalAdresCreateDataFactory
from tests.factories.partij import CreatePartijPersoonDataFactory
from tests.validators import DigitaalAdresCreateDataValidator, DigitaalAdresValidator


@pytest.fixture()
def een_partij(client) -> Partij:
    data = CreatePartijPersoonDataFactory()
    return client.partij.create_persoon(data=data)


@pytest.fixture()
def een_digitaal_adres(client, een_partij) -> Partij:
    data = DigitaalAdresCreateDataFactory(
        verstrektDoorBetrokkene=None,
        verstrektDoorPartij__uuid=een_partij["uuid"],
    )
    return client.digitaal_adres.create(data=data)


@pytest.fixture()
def een_geverifieerd_digitaal_adres(client, een_partij) -> Partij:
    data = DigitaalAdresCreateDataFactory(
        verstrektDoorBetrokkene=None,
        verstrektDoorPartij__uuid=een_partij["uuid"],
        verificatieDatum="2026-09-08",
    )
    return client.digitaal_adres.create(data=data)


@pytest.mark.vcr
def test_create_digitaal_adres(client, een_partij) -> None:
    data = DigitaalAdresCreateDataValidator.validate_python(
        {
            "adres": "foo@bar.com",
            "omschrijving": "professional",
            "soortDigitaalAdres": "email",
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": {"uuid": een_partij["uuid"]},
            "referentie": "portaalvoorkeur",
            "verificatieDatum": "2026-09-08",
        }
    )
    resp = client.digitaal_adres.create(
        data=data,
    )

    DigitaalAdresValidator.validate_python(resp)
    assert resp["adres"] == "foo@bar.com"
    assert resp["omschrijving"] == "professional"
    assert resp["soortDigitaalAdres"] == "email"
    assert resp["verstrektDoorBetrokkene"] is None
    assert resp["verstrektDoorPartij"] == {
        "uuid": een_partij["uuid"],
        "url": een_partij["url"],
    }
    assert resp["referentie"] == "portaalvoorkeur"
    assert resp["verificatieDatum"] == "2026-09-08"


@pytest.mark.usefixtures("een_geverifieerd_digitaal_adres")
@pytest.mark.vcr
def test_list_digitaal_adres(client) -> None:
    resp = client.digitaal_adres.list()
    TypeAdapter(PaginatedResponseBody[DigitaalAdres]).validate_python(resp)


@pytest.mark.vcr
def test_retrieve_geverifieerd_digitaal_adres(
    client, een_geverifieerd_digitaal_adres
) -> None:
    resp = client.digitaal_adres.retrieve(een_geverifieerd_digitaal_adres["uuid"])
    TypeAdapter(DigitaalAdres).validate_python(resp)


@pytest.mark.vcr
def test_partial_update(client, een_digitaal_adres):
    target_is_standaard_adres = True
    target_omschrijving = "New description"
    target_referentie = "portaalvoorkeur"
    target_verificatie_datum = "2026-09-08"
    assert een_digitaal_adres["isStandaardAdres"] != target_is_standaard_adres
    assert een_digitaal_adres["omschrijving"] != target_omschrijving
    assert een_digitaal_adres["referentie"] != target_referentie
    assert een_digitaal_adres["verificatieDatum"] != target_verificatie_datum

    resp = client.digitaal_adres.partial_update(
        een_digitaal_adres["uuid"],
        data={
            "isStandaardAdres": target_is_standaard_adres,
            "omschrijving": target_omschrijving,
            "referentie": target_referentie,
            "verificatieDatum": target_verificatie_datum,
        },
    )

    TypeAdapter(DigitaalAdres).validate_python(resp)
    assert resp["isStandaardAdres"] == target_is_standaard_adres
    assert resp["omschrijving"] == target_omschrijving
    assert resp["referentie"] == target_referentie
    assert resp["verificatieDatum"] == target_verificatie_datum
