from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from rgd.models import ChecksumFile


class DatasetRun(TimeStampedModel):
    """A run of the danesfield algorithm on a dataset."""

    class Status(models.TextChoices):
        CREATED = 'created', _('Created but not queued')
        QUEUED = 'queued', _('Queued for processing')
        RUNNING = 'running', _('Running')
        FAILED = 'failed', _('Failed')
        SUCCEEDED = 'success', _('Succeeded')

    dataset = models.ForeignKey('Dataset', related_name='runs', on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, default=Status.QUEUED, max_length=16)

    # Outputs
    output_log = models.TextField()
    output_files = models.ManyToManyField(ChecksumFile)


class Dataset(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    # For imageless run
    imageless = models.BooleanField(default=True)
    point_cloud_file = models.ForeignKey(
        ChecksumFile, on_delete=models.SET_NULL, null=True, related_name='imageless_datasets'
    )

    # For image run
    files = models.ManyToManyField(ChecksumFile, related_name='image_datasets')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(imageless=True, point_cloud_file__isnull=False)
                    | models.Q(imageless=False, point_cloud_file__isnull=True)
                ),
                name='distinct_imageless',
            )
        ]

    def run_danesfield(self) -> DatasetRun:
        """Dispatch a run of this dataset, returning the DatasetRun object."""
        # Prevent circular import
        from danesfield.core.tasks import run_danesfield

        run: DatasetRun = DatasetRun.objects.create(dataset=self)
        run_danesfield.delay(dataset_run_id=run.pk)

        return run
