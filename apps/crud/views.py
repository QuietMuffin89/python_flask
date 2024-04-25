from flask import Blueprint, render_template, redirect, url_for
from apps.crud.forms import UserForm
from apps.app import db
from apps.crud.models import User


crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)



@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
def sql():
    # user = User(   #INSERT할 때 객체를 작성해서 db세션에 추가하고 커밋하여 변경을 반영해야함
    # username="사용자명",
    # email="flask@wdfd.com",
    # password="qlalfqjsgh"
    # )

    # db.session.add(user)
    # db.session.commit()
    # db.session.query(User).filter_by(id=2, username="admin").all()
    return "콘솔 로그를 확인해 주세요"

@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    form = UserForm()

    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/users")
def users():
    '''사용자의 알람을 취득'''
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('crud.users'))
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))