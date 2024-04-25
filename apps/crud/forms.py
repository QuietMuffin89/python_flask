from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
#validators : 유효성 검사(비밀번호가 짧습니다.)
#DataRequired : 이 필드는 반드시 값을 써야하는 필드
#Email : 이메일 형식을 반드시 지켜야 하는 필드
#사용자 신규작성 및 사용자 편집 폼 클래스
#Length : 입력한 값의 길이 관련
class UserForm(FlaskForm):
    #사용자 폼의 username속성의 라벨과 검증을 설정
    username = StringField(
        "사용자명",
        validators=[
            DataRequired(message="사용자명 필수"),
            Length(max=30, message="30문자 이내로 입력")
        ],
    )
    #사용자 폼 email 속성의 라벨과 검증
    email = StringField(
        "메일주소",
        validators=[
            DataRequired(message="메일 주소는 필수"),
            Email(message="메일주소 형식으로 입력"),
        ],
    )
    #사용자 폼 password 속성의 라벨과 검증
    password = PasswordField(
        "비밀번호",
        validators=[DataRequired(message="빌밀번호 필수")]
    )
    #사용자 폼 submit의 문구 설정
    submit = SubmitField("신규등록")