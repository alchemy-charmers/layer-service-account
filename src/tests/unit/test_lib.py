#!/usr/bin/python3


class TestLib():

    def test_pytest(self):
        assert True

    def test_serviceaccount(self, libserviceaccount):
        ''' See if the helper fixture works to load charm configs '''
        assert isinstance(libserviceaccount.charm_config, dict)
        assert isinstance(libserviceaccount.layer_config, dict)

    def test_install_deps(self, libserviceaccount, mock_apt_install):
        libserviceaccount.install_deps()
        mock_apt_install.assert_called_once()
        mock_apt_install.assert_called_with('passwd')

#    def test_update_accounts(self, libserviceaccount):
#        libserviceaccount.update_accounts()
#        assert isinstance(libserviceaccount.system_passwd, list), "Parsed system passwd db is actually a list"
#        assert len(libserviceaccount.system_passwd) > 0, "Parsed system passwd db is not empty"
#        assert isinstance(libserviceaccount.system_groups, list), "Parsed system group list is actually a list"
#        assert len(libserviceaccount.system_groups) > 0, "Parsed system group list is not empty"
