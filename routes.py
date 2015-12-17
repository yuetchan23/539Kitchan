
from flask import Flask, render_template, request, url_for, redirect
from forms import ContactForm
from flask.ext.mail import Message, Mail
import paypalrestsdk

app = Flask(__name__)

app.secret_key = 'WebDesign'

app.config.update(dict(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME='umsiwebdesign@gmail.com',
        MAIL_PASSWORD='105sstate',
))

mail = Mail(app)

paypalrestsdk.configure({
    'mode': 'sandbox',
    'client_id':'ATz4mp9TIdneVpte7sYtFqa34K4MlORyjsBFEOt1HsYKhirClyFYrcOimZY5OSF1LmrK_Rulsz_mFqiB',
    'client_secret': 'EJdcPSCzW_AFnkBK2rmqLZrYAC3HBXY7k6VIktn3kYtzZP2YTydTx61kek_5i79XZ5p6kZF0lH3Uwc_l'
})

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html',title='Home', name='home')


@app.route('/diy')
def diy():
    return render_template('MakeUrOwn.html', title='DIY', name='DIY')

@app.route('/play')
def play():
    return render_template('play.html', title='Play', name='play')

@app.route('/combo')
def combo():
    return render_template('combo_detail.html', title='Combos', name='combos')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        msg = Message(form.subject.data, sender="umsiwebdesign@gmail.com", recipients=["yidihong@umich.edu"])
        msg1 = Message("Information sent", sender='yidihong@umich.edu', recipients=[form.email.data])
        msg.body = """
        From: %s <%s>
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)
        mail.send(msg1)

        form.name.data = ""
        form.email.data = ""
        form.subject.data = ""
        form.message.data = ""

        return render_template('contact.html', title='contact', name='contact', form=form, message="Thank you for submitting.")
        # return redirect(url_for('contact') )

    elif request.method == 'GET':
        return render_template('contact.html',title='contact', name='contact', form=form)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        if request.args.get('id', None):
            print request.form['combo-name']
            print request.form['combo-price']
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"},
                "redirect_urls": {
                    # note: need modified after deploying
                    "return_url": "http:localhost:5000/pay?success=true",
                    "cancel_url": "http:localhost:5000/pay?success=false"
                },
                "transactions": [ {
                    # ItemList
                    "item_list": {
                        "items": [{
                            "name": request.form['combo-name'],
                            "sku": request.form['combo-name'],
                            "price": request.form['combo-price'],
                            "currency": "USD",
                            "quantity": 1}]},

                    # Amount
                    # Let's you specify a payment amount.
                    "amount": {
                        "total": request.form['combo-price'],
                        "currency": "USD"},
                    "description": "This is the payment transaction description."}]})

            print payment
            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        redirect_url = str(link.href)
                        return redirect(redirect_url)
            else:
                return "redirect failed"
        else:
            return render_template('payment.html')
    elif request.method == 'GET':
        if request.args.get('success', None) == 'true':
            payment = paypalrestsdk.Payment.find(request.args.get('paymentId'))
            payment.execute({"payer_id": request.args.get('PayerID')})
            return render_template('confirm.html')
        elif request.args.get('success', None) == 'false':
            return "false"
        else:
            return render_template('payment.html', title='Pay', name='pay')


if __name__ == '__main__':
    app.run(debug=True)
