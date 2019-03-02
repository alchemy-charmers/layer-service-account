import imp
import mock


def test_update_action(libserviceaccount, monkeypatch):
    mock_function = mock.Mock()
    monkeypatch.setattr(libserviceaccount, 'update_accounts', mock_function)
    assert mock_function.call_count == 0
    imp.load_source('update', './actions/update')
    assert mock_function.call_count == 1
