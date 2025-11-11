import factory
import factory.faker
import factory.fuzzy

from openklant_client.factories.common import ForeignKeyRef
from openklant_client.factories.helpers import FuzzyLiteral, validator
from openklant_client.types.resources.betrokkene import (
    BetrokkeneCreateDataValidator,
    BetrokkeneRol,
)


class ContactnaamFactory(factory.Factory):
    class Meta:
        model = dict

    voorletters = factory.Faker("prefix")
    voornaam = factory.Faker("first_name")
    voorvoegselAchternaam = factory.Faker("prefix")
    achternaam = factory.Faker("last_name")


@validator(BetrokkeneCreateDataValidator)
class BetrokkeneCreateDataFactory(factory.Factory):
    class Meta:
        model = dict

    wasPartij = factory.SubFactory(ForeignKeyRef)
    hadKlantcontact = factory.SubFactory(ForeignKeyRef)
    bezoekadres = None
    correspondentieadres = None
    contactnaam = factory.SubFactory(ContactnaamFactory)
    rol = FuzzyLiteral(BetrokkeneRol)
    organisatienaam = factory.Faker("company")
    initiator = factory.fuzzy.FuzzyChoice((True, False))
