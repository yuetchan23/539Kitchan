from flask.ext.wtf import Form
from wtforms.fields import StringField, TextAreaField, SubmitField


class ContactForm(Form):
  name = StringField("Name")
  email = StringField("Email")
  subject = StringField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")
