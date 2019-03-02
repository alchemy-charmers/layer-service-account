#!/usr/bin/python3
from mock import call


def test_pytest():
    assert True


def test_serviceaccount(libserviceaccount):
    ''' See if the helper fixture works to load charm configs '''
    assert isinstance(libserviceaccount.charm_config, dict)
    assert isinstance(libserviceaccount.layer_config, dict)


def test_install_deps(libserviceaccount, mock_apt_install):

    libserviceaccount.install_deps()

    mock_apt_install.assert_called_once()
    mock_apt_install.assert_called_with('passwd')


def test_update_accounts(libserviceaccount, mock_check_call):

    libserviceaccount.update_accounts()

    # data structure checks
    assert isinstance(libserviceaccount.system_passwd, list), "Parsed system passwd db is actually a list"
    assert len(libserviceaccount.system_passwd) > 0, "Parsed system passwd db is not empty"
    assert isinstance(libserviceaccount.system_groups, list), "Parsed system group list is actually a list"
    assert len(libserviceaccount.system_groups) > 0, "Parsed system group list is not empty"
    assert isinstance(libserviceaccount.accounts, dict), "Parsed charm and layer options are a dict"
    assert len(libserviceaccount.accounts.keys()) > 0, "Parsed charm and layer options groups contain more than one entry"
    assert isinstance(libserviceaccount.groups, dict), "Parsed charm and layer options are a dict"
    assert len(libserviceaccount.groups.keys()) > 0, "Parsed charm and layer options groups contain more than one entry"

    # subprocess checks
    mock_check_call.assert_called()
    mock_check_call.assert_has_calls([
        call(['usermod', '-u', '2000', 'ubuntu']),
        call(['useradd', '-N', '-r', '-u', 1030, 'testuser3']),
        call(['useradd', '-N', '-r', '-u', '1000', 'testuser4']),
        call(['usermod', '-u', 1000, 'testuser']),
        call(['useradd', '-N', '-r', 'testuser2']),
        call(['groupadd', '-g', '10000', 'besttestgroup']),
        call(['groupadd', 'worsttestgroup']),
        call(['groupadd', '-g', 1020, 'testgroup']),
        call(['groupadd', '-g', 1000, 'testgroup2']),
        call(['usermod', '-A', '-G', 'testuser2', 'sudo']),
        call(['usermod', '-A', '-G', 'testuser2', 'lxd']),
        call(['usermod', '-A', '-G', 'testgroup2', 'testuser2']),
        call(['usermod', '-A', '-G', 'testgroup2', 'testuser3'])])
    assert mock_check_call.call_count == 13
