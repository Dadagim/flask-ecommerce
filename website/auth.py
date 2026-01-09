from flask import Blueprint, render_template, request, redirect, flash, send_from_directory
from .models import Producer, Customers
from . import db
from werkzeug.utils  import secure_filename
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint("auth",__name__, url_prefix="/auth")


# sign u for the producer and registration
@auth.route('/signup_producer', methods=['POST', 'GET'])
def signup_producer():
    if request.method == 'POST':
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password= request.form.get("password")
        conform_password = request.form.get("conform-password")
        short_bio = request.form.get("bio")
        phone_number = request.form.get("phone_number")
        profile_picture = request.files["profile_pic"]# it is not loading the image into the server
        print(profile_picture)# none

        if not fullname or not email or not phone_number or not password or not conform_password or not short_bio:# because the pic is none the condition is true
            flash("All fields are required")
            return redirect('/signup_producer')
        elif password != conform_password:
            flash("password miss match")
            return redirect('/signup_producer')
        else:
            new_producer = Producer()
            new_producer.producer_name = fullname.title()
            new_producer.email = email
            new_producer.password = conform_password
            new_producer.phone_number = phone_number
            new_producer.bio = short_bio


            file_name = secure_filename(profile_picture.filename)

            file_path = f'./media/profiles/{file_name}'
            profile_picture.save(file_path)

            new_producer.profile_picture = file_path
            try:
                db.session.add(new_producer)
                db.session.commit()
                flash("you are successfully signed please login")
                return redirect('/login_producer')
            except Exception as e:
                print(e)
                flash("something gone wrong. you are not signed.")
                return redirect("/")
    return render_template("signup.html")


#login the producer
@auth.route("/login_producer", methods=['POST', "GET"])
def login_producer():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email  or not password:
            flash("fill the forms correctly")
            return redirect("/")

        producer = Producer.query.filter_by(email=email).first()
        if producer:
            if producer.validate_password(password=password):
                try:
                    login_user(producer)
                    flash("you have successfully logged in")
                    return redirect("/")
                except Exception as e:
                    print(e)
            else:
                flash("Incorrect password or email")
                return redirect("/")
        else:
            flash("the account doesn't exist")
            return redirect("/login")
    return render_template("login.html")



@auth.route("/signup_customer", methods=['POST', 'GET'])
def signup_customer():
    if request.method == 'POST':
        full_name = request.form.get("fullname").title()
        email = request.form.get("email")
        password = request.form.get("password")
        conform_password = request.form.get("conform-password")
        phone_number = request.form.get("phone_number")
        location = request.form.get("location")

        if not full_name or not email or not password or not conform_password or not phone_number:
            flash("A field is missing")
            return redirect('/')
        elif password != conform_password:
            flash("password miss matched")
            return redirect("/")
        else:
            new_customer = Customers()
            new_customer.user_name=full_name
            new_customer.email=email
            new_customer.password=conform_password
            new_customer.phone_number=phone_number
            new_customer.is_producer=False
            new_customer.location=location
            try:
                db.session.add(new_customer)
                db.session.commit()
                flash("you are registered successfully")
                return redirect("/")
            except Exception as e:
                flash("something went wrong")
                print(e)
                return redirect("/signup_customer")


    return render_template("signup_customer.html")


@auth.route("/login_customer", methods=['GET', 'POST'])
def login_customer():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("a field is missing")
            return redirect("/login_producer")

        customer = Customers.query.filter_by(email=email).first()
        if customer:
            if customer.validate_password(password):
                try:
                    login_user(customer)
                    flash("Welcome to Dagi-Express.")
                    return redirect('/')
                except Exception as e:
                    print(e)
                    flash("something went wrong")
                    return redirect("/")
            flash("invalid password")
        else:
            flash("Account doesn't exist")
            return redirect("/login_customer")

    else:
        return render_template("login_customer.html")



@auth.route("/logout")
@login_required
def logout_customer():
    logout_user()
    flash("logged out ")
    return redirect("/")

@auth.route("/media/profiles/<path:filepath>")
@login_required
def media(filepath):
    return send_from_directory('../media/profiles', filepath)

@auth.route('/profile/<int:usr_id>')
@login_required
def profile(usr_id):
    user = Producer.query.get(usr_id)
    return render_template("profile.html", user=user)
@auth.route("/first")
def first():
    return render_template("first.html")


@auth.route("/change-password/<int:usr_id>", methods=['GET', 'POST'])
@login_required
def change_password(usr_id):
    if request.method == "POST":
        current_password = request.form.get("current-password")
        new_password = request.form.get("new-password")
        conform_password = request.form.get("conform-password")

        if not current_password or not new_password or not conform_password:
            flash("A Field is missing.")
            return redirect("/change-password")

        user = Producer.query.get(usr_id)

        if user.validate_password(current_password):
            if new_password== conform_password:
                try:
                    user.hash_password = conform_password
                    db.session.commit()
                    flash("password updated successfully.")
                    return redirect("/profile")
                except Exception as e:
                    print(e)
                    flash("something went wrong")
                    return redirect("/profile")
            else:
                flash("Passwords doesn't match.")
                return redirect("/profile")
    # design the change password form and template and make it render
