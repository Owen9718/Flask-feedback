from flask import Flask, render_template, redirect, session
from models import connect_db,User,db,Feedback
from forms import Register,Login,FeedbackForm,DeleteForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"


connect_db(app)



@app.route("/")
def register():

    return redirect("/register")


@app.route("/register", methods=["GET","POST"])
def register_user():
    form = Register()
    

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        new_user = User.register(username,password,first_name,last_name,email)

        db.session.commit()
        session['username'] = new_user.username
        
        return redirect("/users/<username>")


    return render_template("register.html",form=form)


@app.route("/users/<username>")
def secret(username):
    if 'username' not in session or username != session['username']:
        return redirect('/login')
    form = DeleteForm()
    user = User.query.get(username)
    return render_template('user.html',user=user,form=form)


@app.route("/login", methods=["GET","POST"])
def login_user():
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")


    return render_template("login.html",form=form)


@app.route("/logout")
def logout_user():
    session.pop('username')

    return redirect('/')


@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")



# @app.route("/users/<username>/delete")



@app.route("/users/<username>/feedback/add", methods=["GET","POST"])
def create_feedback(username):
    if 'username' not in session or username != session['username']:
        return redirect('/')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")


    else:
        return render_template('new_feedback.html',form=form)
    