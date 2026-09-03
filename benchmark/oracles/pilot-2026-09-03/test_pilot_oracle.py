import pytest

import flask


def test_p01_ipv6_server_name_keeps_host_and_port(monkeypatch):
    called = {}
    app = flask.Flask(__name__)
    app.config["SERVER_NAME"] = "[2001:db8::7]:8443"

    def run_simple(host, port, application, **options):
        called.update(host=host, port=port)

    monkeypatch.setattr("werkzeug.serving.run_simple", run_simple)
    app.run()

    assert called == {"host": "2001:db8::7", "port": 8443}


def test_p02_popped_signal_runs_after_teardown_error():
    app = flask.Flask(__name__)
    events = []

    @app.teardown_appcontext
    def fail_teardown(error):
        events.append("teardown")
        raise ValueError("expected teardown failure")

    def on_popped(sender):
        events.append("popped")

    with flask.appcontext_popped.connected_to(on_popped, app):
        ctx = app.app_context()
        ctx.push()

        with pytest.raises(BaseException):
            ctx.pop()

    assert events == ["teardown", "popped"]


def test_p03_explicit_options_enable_beats_disabled_default():
    app = flask.Flask(__name__)
    app.config["PROVIDE_AUTOMATIC_OPTIONS"] = False

    def index():
        return "ok"

    app.add_url_rule("/", view_func=index, provide_automatic_options=True)

    rule = next(rule for rule in app.url_map.iter_rules() if rule.rule == "/")

    assert "OPTIONS" in rule.methods


@pytest.mark.parametrize("filename", ["ACCOUNT.HTML", "icon.SvG", "feed.Xml"])
def test_p04_autoescape_extension_is_case_insensitive(filename):
    app = flask.Flask(__name__)

    assert app.select_jinja_autoescape(filename) is True
