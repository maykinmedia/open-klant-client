import random

import factory
import factory.faker
from faker import Faker

from openklant_client.tests.factories.common import ForeignKeyRef
from openklant_client.tests.factories.helpers import validator
from openklant_client.tests.validators import DigitaalAdresCreateDataValidator

fake = Faker("nl_NL")


@validator(DigitaalAdresCreateDataValidator)
class DigitaalAdresCreateDataFactory(factory.Factory):
    class Meta:
        model = dict

    adres = factory.LazyAttribute(
        lambda obj: (
            fake.email()
            if obj.soortDigitaalAdres == "email"
            else (
                "0912345678"
                if obj.soortDigitaalAdres == "telefoonnummer"
                else fake.address()
            )
        )
    )
    omschrijving = factory.Faker("word")
    soortDigitaalAdres = random.choice(  # noqa: S311
        ["email", "telefoonnummer", "overig"],
    )
    verstrektDoorBetrokkene = factory.SubFactory(ForeignKeyRef)
    verstrektDoorPartij = factory.SubFactory(ForeignKeyRef)
