import factory
import factory.faker
import factory.fuzzy

from tests.factories.common import IdentificationNumber
from tests.factories.helpers import validator
from tests.validators import CreateKlantContactDataValidator


@validator(CreateKlantContactDataValidator)
class CreateKlantContactDataFactory(factory.Factory):
    class Meta:
        model = dict

    nummer = IdentificationNumber()
    kanaal = factory.Faker("word")
    onderwerp = factory.Faker("word")
    inhoud = factory.Faker("sentence")
    taal = "nld"
    indicatieContactGelukt = factory.fuzzy.FuzzyChoice((True, False, None))
    vertrouwelijk = factory.fuzzy.FuzzyChoice((True, False))
    plaatsgevondenOp = factory.LazyFunction(
        lambda: factory.Faker(
            "date_time_between",
            start_date="-1y",
            end_date="now",
        )
        .evaluate(None, None, {"locale": None})
        .isoformat()
    )
