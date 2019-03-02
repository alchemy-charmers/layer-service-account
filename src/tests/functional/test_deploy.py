import pytest
import os
import yaml
from juju.model import Model

# Treat tests as coroutines
pytestmark = pytest.mark.asyncio

# Load charm metadata
metadata = yaml.load(open("./metadata.yaml"))
juju_repository = os.getenv('JUJU_REPOSITORY',
                            '.').rstrip('/')
charmname = metadata['name']
series = ['bionic', 'xenial']


@pytest.fixture
async def model():
    model = Model()
    await model.connect_current()
    yield model
    await model.disconnect()


@pytest.mark.parametrize('series', series)
async def test_serviceaccount_deploy(model, series):
    # this has been modified from the template, as the template
    # deploys from the layer, rather than the built charm, which
    # needs to be fixed
    app = await model.deploy('{}/builds/{}'.format(
            juju_repository,
            charmname),
        series=series)
    await model.block_until(lambda: app.status == 'active')
    assert True
