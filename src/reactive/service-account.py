from charms.reactive import (
    when,
    when_not,
    remove_state,
    set_state
)
from libserviceaccount import ServiceAccountHelper

serviceaccount = ServiceAccountHelper()


# make sure tools are installed
@when_not('layer-service-account.installed')
def install_layer_user():
    serviceaccount.install_deps()
    set_state('layer-service-account.installed')


# apply changes to configuration
@when('config.changed')
def update_accounts():
    remove_state('layer-service-account.configured')
    serviceaccount.update_accounts()
    set_state('layer-service-account.configured')
