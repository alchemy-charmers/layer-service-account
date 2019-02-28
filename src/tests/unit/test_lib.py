#!/usr/bin/python3

from charmhelpers.core import unitdata

class TestLib():
    def test_pytest(self):
        assert True

    def test_serviceaccount(self, libserviceaccount):
        ''' See if the helper fixture works to load charm configs '''
        assert isinstance(libserviceaccount.charm_config, dict)
        assert isinstance(libserviceaccount.layer_config, dict)

    # Include tests for functions in libserviceaccount
