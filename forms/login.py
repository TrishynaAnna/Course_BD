from flask_wtf import Form
from wtforms import StringField, SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators


class Login(Form):

   person_login = StringField("Login: ",[
                                    validators.DataRequired("Please enter your Login."),
                                    validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                                 ])

   person_password = StringField("Password: ",[
                                    validators.DataRequired("Please enter your password."),
                                    validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                                 ])

   submit = SubmitField("Sign up")