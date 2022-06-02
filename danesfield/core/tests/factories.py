from django.contrib.auth.models import User
import factory.django
import factory.fuzzy
from rdoasis.algorithms.models import Dataset
from rdoasis.algorithms.tests.factories import DatasetFactory
from rgd.models.common import ChecksumFile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.SelfAttribute('email')
    email = factory.Faker('safe_email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class ChecksumFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChecksumFile

    file = factory.django.FileField(data=bytes(b'Test data!'))
    name = factory.LazyAttribute(lambda obj: obj.file.name)


class DanesfieldImagelessDatasetFactory(DatasetFactory):
    @factory.post_generation
    def files(self, create, extracted, **kwargs):
        self.files.set([ChecksumFileFactory() for _ in range(5)])


class DanesfieldImagefulDatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dataset

    name = factory.fuzzy.FuzzyText()
