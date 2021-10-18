from pathlib import Path

from django.contrib.auth.models import User
import factory.django
import factory.fuzzy
from rgd.models.common import ChecksumFile

from danesfield.core.models.dataset import Dataset, DatasetRun

PARENT_DIR = Path(__file__).parent
DATA_DIR = PARENT_DIR / 'data'


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

    file = factory.django.FileField(from_path=(DATA_DIR / 'test.txt'))
    name = factory.LazyAttribute(lambda obj: obj.file.name)


class DatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dataset

    name = factory.fuzzy.FuzzyText()
    imageless = True

    # Not used, just necessary for database constraints
    point_cloud_file = factory.SubFactory(ChecksumFileFactory)


class ImagefulDatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dataset

    name = factory.fuzzy.FuzzyText()
    imageless = False


class DatasetRunFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DatasetRun

    dataset = factory.SubFactory(DatasetFactory)
