import factory
import factory.faker
import factory.fuzzy

from tests.factories.helpers import validator
from tests.validators import CreateOnderwerpObjectDataValidator


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
