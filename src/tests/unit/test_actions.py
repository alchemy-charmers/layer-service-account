import imp
import mock


class TestActions():
    def test_reapply_action(self, libserviceaccount, monkeypatch):
        mock_function = mock.Mock()
        monkeypatch.setattr(libserviceaccount, 'applyaction', mock_function)
        assert mock_function.call_count == 0
        imp.load_source('applyaction', './actions/apply')
        assert mock_function.call_count == 1
