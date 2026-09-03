import flask


def test_p04_dotfile_autoescape_behavior_is_preserved():
    app = flask.Flask(__name__)

    assert app.select_jinja_autoescape(".html") is True
