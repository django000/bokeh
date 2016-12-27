import os
import webbrowser

import pytest
from mock import patch

import bokeh.util.browser as bub

_open_args = None

class _RecordingWebBrowser(object):
    def open(self, *args, **kw):
        global _open_args
        _open_args = args, kw

def test_get_browser_controller_dummy():
    b = bub.get_browser_controller('dummy')
    assert isinstance(b, bub.DummyWebBrowser)

def test_get_browser_controller_None():
    b = bub.get_browser_controller(None)
    assert b == webbrowser

@patch('webbrowser.get')
def test_get_browser_controller_value(mock_get):
    bub.get_browser_controller('foo')
    assert mock_get.called
    assert mock_get.call_args[0] == ("foo",)
    assert mock_get.call_args[1] == {}

@patch('webbrowser.get')
def test_get_browser_controller_dummy_with_env(mock_get):
    os.environ['BOKEH_BROWSER'] = "bar"
    bub.get_browser_controller('dummy')
    assert mock_get.called
    assert mock_get.call_args[0] == ("bar",)
    assert mock_get.call_args[1] == {}
    del os.environ['BOKEH_BROWSER']

@patch('webbrowser.get')
def test_get_browser_controller_None_with_env(mock_get):
    os.environ['BOKEH_BROWSER'] = "bar"
    bub.get_browser_controller(None)
    assert mock_get.called
    assert mock_get.call_args[0] == ("bar",)
    assert mock_get.call_args[1] == {}
    del os.environ['BOKEH_BROWSER']

@patch('webbrowser.get')
def test_get_browser_controller_value_with_env(mock_get):
    os.environ['BOKEH_BROWSER'] = "bar"
    bub.get_browser_controller('foo')
    assert mock_get.called
    assert mock_get.call_args[0] == ("bar",)
    assert mock_get.call_args[1] == {}
    del os.environ['BOKEH_BROWSER']

def test_view_bad_new():
    with pytest.raises(RuntimeError) as e:
        bub.view("foo", new="junk")
        assert str(e) == "invalid 'new' value passed to view: 'junk', valid values are: 'same', 'window', or 'tab'"

def test_view_args():
    db = bub.DummyWebBrowser
    bub.DummyWebBrowser = _RecordingWebBrowser

    # test http locations used as-is
    bub.view("http://foo", browser="dummy")
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 0})

    # test non-http locations treated as local files
    bub.view("/foo/bar", browser="dummy")
    assert _open_args == (('file:///foo/bar',), {'autoraise': True, 'new': 0})

    # test autoraise passed to open
    bub.view("http://foo", browser="dummy", autoraise=False)
    assert _open_args == (('http://foo',), {'autoraise': False, 'new': 0})

    # test handling of new values
    bub.view("http://foo", browser="dummy", new="same")
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 0})
    bub.view("http://foo", browser="dummy", new="window")
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 1})
    bub.view("http://foo", browser="dummy", new="tab")
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 2})

    bub.DummyWebBrowser = db
