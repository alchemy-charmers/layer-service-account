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
                       'uidmap': {'testuser': 1010, 'testuser3': 1030},
                       'gidmap': {'testgroup': 1020},
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

        # Manually add cfg from other layers
        # cfg['my-other-layer'] = 'mock'
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
    from charmhelpers import fetch

    def mock_apt_install(package):
        return True

    monkeypatch.setattr(
        fetch,
        'apt_install',
        mock_apt_install)


@pytest.fixture
def mock_popen(monkeypatch):
    import subprocess 

    monkeypatch.setattr(
        subprocess,
        'Popen',
        mock.MockPopen())


@pytest.fixture
def libserviceaccount(tmpdir,
                      mock_hookenv_config,
                      mock_charm_dir,
                      mock_layers,
                      mock_apt_install,
                      mock_popen,
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
