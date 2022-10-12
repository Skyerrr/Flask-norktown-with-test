import pytest
from datetime import datetime
from ...app import create_app
from ..models import Person


@pytest.fixture(scope="module")
def app():
    """
    Instance of Main flask app
    """

    return create_app()


@pytest.fixture(scope="module")
def new_user():
    user = Person(
        email="test@test.com", name="test", password="test", date=type(datetime.now())
    )
    return user
