__author__ = 'wdolowicz'


def test_login(app):
    app.session.login("Administrator", "root")
    assert app.session.is_logged_in_as("administrator")