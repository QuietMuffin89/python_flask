from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, url_for, request, redirect, flash
import logging
import os
from flask_mail import Mail, Message
# from flask_debugtoolbar import DebugToolbarExtension

#서버 프로그램 객체를 만든다.
#__name__: 실행 중인 모듈의 시스템 상의 이름
app = Flask(__name__)

app.config["SECRET_KEY"] = "1qpwo2QQPP"
app.logger.setLevel(logging.DEBUG)
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# toolbar = DebugToolbarExtension(app)
# / :기본 주소로 요청이 왔을 때 무엇을 할지 정의하기
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT") #app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)
@app.route("/")
def index() :
    return "Hello, Flask!!"

# @app.route("/hello")
# def hello() :
#     return "Heelo, World!"
#엔드포인트명을 지정하지 않으면 함수명이 엔드포인트명이 된다
#메소드에 따른 처리를 원한다면 구별해서 정의할 수 있다.
@app.route("/hello/<name>",
            methods=["get"],
           endpoint="hello-endpoint")
def hello(name) :
    return f'hello,{name}!!'

# 템플릿 엔진: 웹 서버 프레임워크 중에서는 사용자에게 문서를 전달할 때,
# 빈 칸이 있는 html 문서와 그 빈 칸에 들어갈 데이터를 함께 전달하도록 설계된 경우가 많다.

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="ak", page="1"))

#플라스크의 템플릿 문서는 앱 내 templates 폴더 안에 있다고 가정한다.
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    if request.method == "POST":
        # 폼 데이터 처리
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        send_email(
            email, #메일주소    
            "문의 감사합니다.", # 이메일 답장의 제목
            "contact_mail",  # 이메일 내용의 템플릿
            username=username, # 사용자 이름
            description=description, # 문의 내용
        )

        # 입력 유효성 검사
        is_valid = True
        if not username:
            flash("사용자 명은 필수입니다.")
            is_valid = False

        if not email:
            flash("메일 주소는 필수입니다.")
            is_valid = False
        else:
            try:
                validate_email(email)
            except EmailNotValidError:
                flash("메일 주소의 형식으로 입력해 주세요")
                is_valid = False

        if not description:
            flash("문의 내용은 필수입니다.")
            is_valid = False

        if not is_valid:
            # 입력이 유효하지 않은 경우, 다시 contact 페이지로 리다이렉트하며 데이터 전달
            return redirect(url_for("contact"))
        
        flash("문의해 주셔서 감사합니다.")
        # 입력이 유효한 경우, contact_complete 페이지로 리다이렉트
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")
    # 메일을 보내기 위해서 API사용하는 함수
def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)