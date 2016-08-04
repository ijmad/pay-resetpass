#!/usr/bin/env python

import os
from flask import Flask, render_template, request

import sendgrid
from sendgrid.helpers.mail import *

import bcrypt


app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')
  


@app.route('/', methods=['POST'])
def index_post():
  email = request.form['email']
  password = bcrypt.hashpw(str(request.form['password']), bcrypt.gensalt(14))
  phone = request.form['phone']

  sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
  
  from_email = Email('gov-uk-pay-support@digital.cabinet-office.gov.uk')
  subject = '[AUTOMATED] Change Password'
  to_email = Email(os.environ.get('TO_EMAIL'))
  content = Content("text/plain", 'Login Email: ' + email + '\r\n\r\nNew Password (Hash): ' + password + '.\r\n\r\nPhone Number: ' + phone)
  mail = Mail(from_email, subject, to_email, content)
  response = sg.client.mail.send.post(request_body=mail.get())
  
  print(response.status_code)
  
  return render_template('thanks.html')


if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port, debug=True)

