import factory
import factory.fuzzy

from openklant_client.tests.factories.helpers import validator
from openklant_client.tests.validators import CreateInterneTaakDataValidator


@validator(CreateInterneTaakDataValidator)
class CreateInterneTaakFactory(factory.Factory):
    class Meta:
        model = dict

    nummer = factory.LazyAttributeSequence(lambda o, n: f"{n + 1:010d}")
    gevraagdeHandeling = factory.Faker("word")
    aanleidinggevendKlantcontact = None
    toegewezenAanActor = None
    status = factory.fuzzy.FuzzyChoice(["te_verwerken", "verwerkt"])
