from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired


class NewVehicleForm(FlaskForm):
    """
    This Form is for adding a new vehicle to the Person model
    """

    person_id = SelectField("Person", choices=[], validators=[DataRequired()])
    vehicle_name = SelectField(
        "Vehicle Name",
        choices=["HATCH", "SEDAN", "CONVERTIBLE"],
        validators=[DataRequired()],
    )
    vehicle_color = SelectField(
        "Vehicle Color", choices=["YELLOW", "BLUE", "GRAY"], validators=[DataRequired()]
    )
    sale = SelectField(
        choices=[("True", "Yes"), ("False", "No")],
        validators=[InputRequired()],
    )
    submit = SubmitField("Submit")
