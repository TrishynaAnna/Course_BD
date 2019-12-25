from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class UserGroupForm(Form):

   user_id = IntegerField("User id: ", [
                                    validators.DataRequired("Please enter your id."),
                                    validators.NumberRange(0, 10000, "Name should be from 3 to 20 symbols")
                                 ])

   group_id = IntegerField("Group id: ", [
                                   validators.DataRequired("Please enter your id."),
                                   validators.NumberRange(0, 10000, "Name should be from 3 to 20 symbols")
                               ])


   submit = SubmitField("Save")


