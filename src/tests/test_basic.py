from datetime import datetime


def test_app_is_created(app):
    """
    Test if app is created
    """
    assert app.name == "norktown.app"


def test_config_is_loaded(config):
    """
    Test app configs
    """

    assert config["DEBUG"] is True
    assert config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///person.db"
    assert config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False
    assert config["BOOTSTRAP_USE_MINIFIED"] is True


def test_no_login_routes(client):
    """
    Test not authenticated user routes
    """
    assert client.get("/").status_code == 200
    assert client.get("/person/1").status_code == 200
    assert client.get("/register").status_code == 200
    assert client.get("/login").status_code == 200
    assert client.get("/edit/1").status_code == 403
    assert client.get("/deletevehicle/1/1").status_code == 403


def test_new_user(new_user):
    """
    Test Person models creating new person
    """

    assert new_user.email == "test@test.com"
    assert new_user.name == "test"
    assert new_user.password == "test"
    assert new_user.date == type(datetime.now())
