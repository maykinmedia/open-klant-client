import factory
import factory.faker
import factory.fuzzy

from openklant_client.tests.factories.helpers import validator
from openklant_client.tests.validators import CreateOnderwerpObjectDataValidator


class OnderwerpObjectIdentificatorFactory(factory.Factory):
    class Meta:
        model = dict

    objectId = factory.Faker("ean", length=13)
    codeObjecttype = factory.Faker("word")
    codeRegister = factory.Faker("word")
    codeSoortObjectId = factory.Faker("word")


@validator(CreateOnderwerpObjectDataValidator)
class CreateOnderwerpObjectDataFactory(factory.Factory):
    class Meta:
        model = dict

    wasKlantcontact = None
    klantcontact = None
    onderwerpobjectidentificator = factory.SubFactory(
        OnderwerpObjectIdentificatorFactory
    )
