from charms.reactive import when_not, set_state, hook
from charmhelpers.core.hookenv import application_user_set
from charms import layer


@when_not('layer-user.installed')
def install_layer_user():
    with open(layer.options('user')['file_name'], 'r') as user:
        application_user_set(user.readline().strip())
    set_state('layer-user.installed')


@hook('upgrade-charm')
def update_user():
    with open(layer.options('user')['file_name'], 'r') as user:
        application_user_set(user.readline().strip())
