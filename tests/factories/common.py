import factory
import factory.faker


class ForeignKeyRef(factory.Factory):
    class Meta:
        model = dict

    uuid = factory.Faker("uuid4")


def IdentificationNumber():
    return factory.LazyAttributeSequence(lambda o, n: f"{n + 1:010d}")
