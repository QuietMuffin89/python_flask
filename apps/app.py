from flask import Flask


#create_app 함수 작성
def create_app():
    #플라스크 인스턴스 생성
    app = Flask(__name__)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app