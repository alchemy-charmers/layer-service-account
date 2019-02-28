import imp
import mock


class TestActions():
    def test_update_action(self, libserviceaccount, monkeypatch):
        mock_function = mock.Mock()
        monkeypatch.setattr(libserviceaccount, 'update_accounts', mock_function)
        assert mock_function.call_count == 0
        imp.load_source('update', './actions/update')
        assert mock_function.call_count == 1
