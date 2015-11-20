from flask import Flask, render_template, request  #NEW IMPORT -- request
from forms import ContactForm 					# NEW IMPORT LINE
from flask.ext.mail import Message, Mail

mail = Mail()
app = Flask(__name__)    #This is creating a new Flask object

app.secret_key = 'WebDesign'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'umsiwebdesign@gmail.com'
app.config["MAIL_PASSWORD"] = '105sstate'

mail.init_app(app)
#decorator that links...
@app.route('/')          								#This is the main URL
def default():
    return render_template("index.html", name = "index", title = "HOME PAGE")			#The argument should be in templates folder

@app.route('/index')          								#This is the main URL
def home():
    return render_template("index.html", name = "index", title = "HOME PAGE")			#The argument should be in templates folder

@app.route('/courses')          								#This is the main URL
def courses():
    return render_template("courses.html", name = "courses", title = "COURSES PAGE")			#The argument should be in templates folder

@app.route('/interests')          								#This is the main URL
def interests():
    return render_template("interests.html", name = "interests", title = "INTERESTS PAGE")			#The argument should be in templates folder

@app.route('/other')          								#This is the main URL
def other():
    return render_template("other.html", name = "other", title = "OTHER PAGE")			#The argument should be in templates folder

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def pageNotFound(e):
    return render_template('500.html'), 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    # msg = Message("Hello", sender="colleenvanlent@gmail.com",
    #               recipients=["collemc@umich.edu"])
    # mail.send(msg);

    msg = Message(form.subject.data, sender='contact@example.com', recipients=['colleenvanlent@gmail.com']) #besure to change this to your own test email
    msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
    mail.send(msg)

    return render_template('contact.html', form=form, message="Thank you for sumitting your information")

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)		#debug=True is optional
