from rdoasis.algorithms.models import Algorithm


def danesfield_algorithm() -> Algorithm:
    """Return the singleton Danesfield algorithm."""
    # Purposefully don't catch error, as this Algorithm should always be present
    return Algorithm.objects.get(id=1, name='Danesfield')
