from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()


class Vehicle(db.Model):
    """
    Vehicle model

    relationship many-to-one -> Person

    """

    __tablename__ = "vehicle"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    vehicle_name = db.Column(db.String(100), unique=False, nullable=False)
    vehicle_color = db.Column(db.String(100), unique=False, nullable=False)
    sale = db.Column(db.Boolean, default=False, unique=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Person(UserMixin, db.Model):
    """Person model
    UserMixin provides default implementations for the methods that Flask-Login
    expects user objects to have.

    relationship one-to-many -> Vehicle
    """

    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime)
    vehicle = relationship(
        "Vehicle", backref="vehicle", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
