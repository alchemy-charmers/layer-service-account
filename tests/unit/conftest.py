#!/usr/bin/python3
import mock
import pytest


@pytest.fixture
def mock_layers(monkeypatch):
    import sys
    sys.modules['charms.layer'] = mock.Mock()
    sys.modules['reactive'] = mock.Mock()
    # Mock any functions in layers that need to be mocked here

    def options(layer):
        # mock options for layers here
        print(layer)
        if layer == 'service-account':
            options = {'users': ['testuser', 'testuser2', 'testuser3'],
                       'groups': ['testgroup', 'testgroup2'],
                       'uidmap': {'testuser': 1000, 'testuser3': 1030},
                       'gidmap': {'testgroup': 1020, 'testgroup2': 1000},
                       'membership': {'testgroup2': ['testuser2', 'testuser3']}
                       }
            return options
        else:
            return None

    monkeypatch.setattr('libserviceaccount.layer.options', options)


@pytest.fixture
def mock_hookenv_config(mock_layers, monkeypatch):
    import yaml

    def mock_config():
        cfg = {}
        yml = yaml.load(open('./config.yaml'))

        # Load all defaults
        for key, value in yml['options'].items():
            cfg[key] = value['default']

        # for testing full extent of parsing without
        # having luxurious defaults specified in config.yaml
        cfg['system-group-membership'] = 'testuser=lxd,testuser2=sudo:lxd'
        cfg['system-additional-users'] = 'ubuntu,testuser3,testuser4'
        cfg['system-additional-groups'] = 'besttestgroup,worsttestgroup'
        cfg['system-uidmap'] = 'testuser3=1000,testuser4=5000,testuser=1006,ubuntu=2000,testuser4=1000,testuser5=1000'
        cfg['system-gidmap'] = 'besttestgroup=10000,testgroup=1030,testgroup2=1040,ubuntu=2000'

        return cfg

    monkeypatch.setattr('libserviceaccount.hookenv.config', mock_config)


@pytest.fixture
def mock_remote_unit(monkeypatch):
    monkeypatch.setattr(
        'libserviceaccount.hookenv.remote_unit',
        lambda: 'unit-mock/0')


@pytest.fixture
def mock_charm_dir(monkeypatch):
    monkeypatch.setattr(
        'libserviceaccount.hookenv.charm_dir',
        lambda: '/mock/charm/dir')


@pytest.fixture
def mock_apt_install(monkeypatch):

    mocked_apt_install = mock.Mock(
        returnvalue=True)

    monkeypatch.setattr(
        'charmhelpers.fetch.apt_install',
        mocked_apt_install)

    return mocked_apt_install


@pytest.fixture
def mock_check_call(monkeypatch):

    def print_check_call(args, *, kwargs={}):
        print(args)
        return True

    mocked_check_call = mock.Mock()
    mocked_check_call.get.side_effect = print_check_call

    monkeypatch.setattr(
        'libserviceaccount.check_call',
        mocked_check_call)

    return mocked_check_call


@pytest.fixture
def mock_log(monkeypatch):

    mocked_log = mock.Mock()

    monkeypatch.setattr(
        'libserviceaccount.log',
        mocked_log)

    return mocked_log


@pytest.fixture
def libserviceaccount(tmpdir,
                      mock_hookenv_config,
                      mock_charm_dir,
                      mock_layers,
                      mock_apt_install,
                      mock_check_call,
                      mock_log,
                      monkeypatch):
    from libserviceaccount import ServiceAccountHelper
    serviceaccount = ServiceAccountHelper()

    passwd_file = tmpdir.join('example_passwd.cfg')
    with open('./tests/unit/example_passwd', 'r') as src_file:
        passwd_file.write(src_file.read())
    serviceaccount.passwd_path = passwd_file.strpath

    group_file = tmpdir.join('example_group.cfg')
    with open('./tests/unit/example_group', 'r') as src_file:
        group_file.write(src_file.read())
    serviceaccount.groups_path = group_file.strpath

    # Any other functions that load the helper will get this version
    monkeypatch.setattr('libserviceaccount.ServiceAccountHelper', lambda: serviceaccount)

    return serviceaccount
