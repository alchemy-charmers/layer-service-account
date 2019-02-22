#!/usr/bin/python3

from charmhelpers.core import unitdata


class TestLib():
    def test_pytest(self):
        assert True

    def test_serviceaccount(self, libserviceaccount):
        ''' See if the helper fixture works to load charm configs '''
        assert isinstance(libserviceaccount.charm_config, dict)

    def test_serviceaccount_kv(self, libserviceaccount):
        ''' See if the unitdata kv helper is loaded '''
        assert isinstance(libserviceaccount.kv, unitdata.Storage)

    # Include tests for functions in libserviceaccount
