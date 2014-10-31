from flask import Flask, render_template, redirect, request, flash, session
import jinja2
import model

app = Flask(__name__)
app.secret_key = 'sdjfdksljfkslfjfdksljfdkasdjf'
app.jinja_env.undefined = jinja2.StrictUndefined



@app.route("/")
def displaylogin():
    return render_template("login.html")

@app.route("/signupform")
def displaysignup():
    return render_template("signupform.html")

@app.route("/users")
def index():
    user_list = model.session.query(model.User).limit(25).all()
    return render_template("user_list.html", user_list = user_list)

@app.route("/home/<int:id>")
def home(id):
    rating_list = model.session.query(model.Rating).filter_by(user_id = id).all()
    # for rating in rating_list:
    #     print rating.movie.name
    return render_template("home.html", rating_list = rating_list)

@app.route("/signup", methods=["POST"])
def signupprocess():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    check_duplicate = model.session.query(model.User).filter_by(email = email).all()
    if check_duplicate != []:
        flash("There is already an account linked to this email. Please login.")
        return render_template("login.html")
    else:
        user = model.User()
        user.age = age
        user.zipcode = zipcode
        user.email = email
        user.password = password
        model.session.add(user)
        model.session.commit()
        flash("Thanks for signing up! Please login.")
        return render_template("login.html")

@app.route("/login", methods=['POST'])
def loginprocess():
    email = request.form.get("email")
    password = request.form.get("password")
    print email
    print password
    validate_user = model.session.query(model.User).filter_by(email = email).all()
    print validate_user
    if validate_user == []:
        flash("You don't have an account. Please signup.")
        return redirect("/signupform")
    else:
        if validate_user[0].password != password:
            flash("Your email and password don't match an account. Please reenter a valid email and password.")
            return redirect("/")
        else:
            session['user_id'] = validate_user[0].id
            print session['user_id']
            #add to html to incorporate flash
            flash("Welcome,", email)
            return redirect("/home/1")


@app.route("/movies")
def movie_index():
    movie_list = model.session.query(model.Movie).all()
    return render_template("movie_list.html", movie_list = movie_list)

@app.route("/updaterating/<int:movie_id>")
def displayratingform(movie_id):
    movie = model.session.query(model.Movie).filter_by(id = movie_id).first()
    title = movie.name
    return render_template("rating_form.html", title = title, movieid = movie_id)

@app.route("/ratingprocess", methods = ["POST"])
def ratingprocess():
    movie_title = request.form.get("movietitle")
    movie_id = request.form.get("movieid")
    rating = request.form.get("rating")
    print session
    rating_object = model.session.query(model.Rating).filter_by(movie_id = movie_id).filter_by(user_id = session['user_id']).first()
    rating_object.rating = rating
    model.session.commit()
    flash("You've successfully updated your rating for %s!" % movie_title)
    return redirect("/home")

@app.route("/addrating/<int:id>")
def displayaddratingform(id):
    movie = model.session.query(model.Movie).filter_by(id = id).first()
    title = movie.name
    user = model.session.query(model.User).filter_by(id = session['user_id']).first()
    prediction = model.User.make_prediction(user, movie.id)
    return render_template("addratingform.html", title = title, movieid = id, prediction = prediction)

@app.route("/addratingprocess", methods=["POST"])   
def add_rating():
    movie_title = request.form.get("movietitle")
    movie_id = request.form.get("movieid")
    rating = request.form.get("rating")
    newrating = model.Rating()
    newrating.movie_id = movie_id
    newrating.rating = rating
    newrating.user_id = session['user_id']
    model.session.add(newrating)
    model.session.commit()
    flash("You've successfully added a rating for %s!" % movie_title)
    return redirect("/home")

if __name__ == "__main__":
    app.run(debug = True)