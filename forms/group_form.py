from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class GroupForm(Form):

   group_id = IntegerField("Id: ", [
                                    validators.DataRequired("Please enter your id."),
                                    validators.NumberRange(0, 10000, "Name should be from 3 to 20 symbols")
                                 ])

   group_name = StringField("Name: ", [
                                   validators.DataRequired("Please enter your name."),
                                   validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                               ])

   group_topic = StringField("Topic: ", [
                                   validators.DataRequired("Please enter your topic."),
                                   validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                               ])

   submit = SubmitField("Save")


