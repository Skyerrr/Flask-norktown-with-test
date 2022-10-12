from datetime import datetime
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, abort, Blueprint
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import Person, Vehicle, db
from src.forms import NewVehicleForm

routes = Blueprint(
    "routes", __name__, static_folder="src/static", template_folder="src/templates"
)


def admin_only(f):
    """
    This decorator function checks if current logged user is id 1
    if not return error code 403
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.id != 1:
                return abort(403)
        except AttributeError:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@routes.route("/", methods=["GET"])
def get_all_persons() -> str:
    """
    Function View for displaying main page with all registered persons in Person model.
    Returns the index template with all_persons variable
    """

    all_persons = Person.query.order_by(Person.id).all()

    return render_template("index.html", all_persons=all_persons)


@routes.route("/person/<int:person_id>", methods=["GET"])
def show_person(person_id: int) -> str:
    """
    Function View for displaying person page with specific person from Person model.
    Returns the index template with person variable

    param:
    person_id requested id from route
    requested_person Person query model from Person model
    """

    requested_person = Person.query.get(person_id)

    return render_template("person.html", person=requested_person)


@routes.route("/edit/<int:person_id>", methods=["GET", "POST"])
@admin_only
def edit_person(person_id: int) -> str:
    """
    This function purpose is to add or delete a Vehicle model of a person based on id sent from previously page(routes.show_person)
    Search Person model by id from person_id arg, render form from NewVehicleForm, validates and flash
    a message if person tries to add more than of 3 vehicles. Return user to the same page.

    param:
    person_edit = Person query based from person_id arg
    form = form from class NewVehicleForm
    """

    person_edit = Person.query.get(person_id)
    form = NewVehicleForm()
    form.person_id.choices = [(person_edit.id, person_edit.name)]
    if form.validate_on_submit():
        if len(person_edit.vehicle) > 2:
            flash("Max 3 vehicles", "failed")

        else:
            if request.form["sale"] == "True":
                sale = True
            else:
                sale = False
            new_vehicle = Vehicle(
                person_id=request.form["person_id"],
                vehicle_name=request.form["vehicle_name"],
                vehicle_color=request.form["vehicle_color"],
                sale=sale,
            )
            db.session.add(new_vehicle)
            db.session.commit()
            flash("Vehicle Successfully Added", "succes")

        return render_template("edit.html", form=form, person=person_edit)
    return render_template("edit.html", form=form, person=person_edit)


@routes.route("/register", methods=["GET", "POST"])
def register() -> str:
    """
    This function tries to register a new Person model if the email is not already in use,
    if email is already in use redirects the user to the login page.
    Hash and salt password for secure database
    Saves created datetime in Person model.
    Then calls response object to redirects the user to home page(routes.get_all_persons)
    """

    if request.method == "POST":

        if Person.query.filter_by(email=request.form.get("email")).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("routes.login"))

        hash_and_salted_password = generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=8
        )
        new_user = Person(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_and_salted_password,
            date=datetime.now(),
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("routes.get_all_persons"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@routes.route("/login", methods=["GET", "POST"])
def login() -> str:
    """
    Tries to authenticate User from Person model using email and password verification.
    If email is not registered flash a message telling email does not exist.
    If password is incorrect flash a message telling password is incorrect.
    If it is correct autheticate the user using passing the user object to flask_login login_user function.
    Then calls response object to redirects the user to home page(routes.get_all_persons)
    """

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Person.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("routes.login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("routes.login"))
        else:
            login_user(user)
            return redirect(url_for("routes.get_all_persons"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@routes.route("/logout")
def logout() -> str:
    """
    Calls flask_login logout_user function and
    return a response object to redirect the user to route get_all_persons
    """

    logout_user()
    return redirect(url_for("routes.get_all_persons"))


@routes.route("/deletevehicle/<int:vehicle_id>/<int:person_id>")
@admin_only
def delete_vehicle(vehicle_id: int, person_id: int) -> str:
    """
    This function deletes vehicle from Vehicle model based in vehicle_id and person_id args
    Then return a response object to redirect the user to the same updated page(routes.edit_person)
    """

    the_person_id = Person.query.get(person_id)
    person_id = the_person_id.id
    vehicle_to_delete = Vehicle.query.get(vehicle_id)
    db.session.delete(vehicle_to_delete)
    db.session.commit()
    return redirect(url_for("routes.edit_person", person_id=person_id))
