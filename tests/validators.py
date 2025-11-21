"""
Pydantic validators for testing API responses.

This module contains TypeAdapters for validating API request and response data
in tests. These validators ensure that the data returned by the API matches
the expected TypedDict schemas.
"""

from pydantic import TypeAdapter

from openklant_client.types.resources.actor import Actor, CreateActorData
from openklant_client.types.resources.betrokkene import Betrokkene, BetrokkeneCreateData
from openklant_client.types.resources.digitaal_adres import (
    DigitaalAdres,
    DigitaalAdresCreateData,
)
from openklant_client.types.resources.interne_taak import (
    CreateInterneTaakData,
    InterneTaak,
)
from openklant_client.types.resources.klant_contact import (
    CreateKlantContactData,
    KlantContact,
)
from openklant_client.types.resources.maak_klant_contact import (
    MaakKlantContact,
    MaakKlantContactCreateData,
)
from openklant_client.types.resources.onderwerp_object import (
    CreateOnderwerpObjectData,
    OnderwerpObject,
)
from openklant_client.types.resources.partij import (
    CreatePartijContactpersoonData,
    CreatePartijOrganisatieData,
    CreatePartijPersoonData,
    Partij,
)
from openklant_client.types.resources.partij_identificator import (
    CreatePartijIdentificatorData,
    PartijIdentificator,
)

# Actor validators
ActorValidator = TypeAdapter(Actor)
CreateActorDataValidator = TypeAdapter(CreateActorData)

# Betrokkene validators
BetrokkeneValidator = TypeAdapter(Betrokkene)
BetrokkeneCreateDataValidator = TypeAdapter(BetrokkeneCreateData)

# Digitaal Adres validators
DigitaalAdresValidator = TypeAdapter(DigitaalAdres)
DigitaalAdresCreateDataValidator = TypeAdapter(DigitaalAdresCreateData)

# Interne Taak validators
InterneTaakValidator = TypeAdapter(InterneTaak)
CreateInterneTaakDataValidator = TypeAdapter(CreateInterneTaakData)

# Klant Contact validators
KlantContactValidator = TypeAdapter(KlantContact)
CreateKlantContactDataValidator = TypeAdapter(CreateKlantContactData)

# Onderwerp Object validators
OnderwerpObjectValidator = TypeAdapter(OnderwerpObject)
CreateOnderwerpObjectDataValidator = TypeAdapter(CreateOnderwerpObjectData)

# Partij validators
PartijValidator = TypeAdapter(Partij)
CreatePartijPersoonDataValidator = TypeAdapter(CreatePartijPersoonData)
CreatePartijOrganisatieDataValidator = TypeAdapter(CreatePartijOrganisatieData)
CreatePartijContactpersoonDataValidator = TypeAdapter(CreatePartijContactpersoonData)

# Partij Identificator validators
PartijIdentificatorValidator = TypeAdapter(PartijIdentificator)
CreatePartijIdentificatorDataValidator = TypeAdapter(CreatePartijIdentificatorData)

#  Maak Klant Contact validators
MaakKlantContactValidator = TypeAdapter(MaakKlantContact)
MaakKlantContactCreateDataValidator = TypeAdapter(MaakKlantContactCreateData)
