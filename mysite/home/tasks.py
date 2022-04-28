# Create your tasks here
from __future__ import absolute_import, unicode_literals
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from celery import shared_task
import json
@shared_task() 
def send_email(user):
    print('In celery')
    user = json.loads(user)
    mail_subject = '회원가입을 위해 아래 링크를 클릭해 주세요'
    message = render_to_string('registration/acc_active_email.html', {
        'user': user["username"],
        'domain': "http://www.buythedip.shop", # current_domain
        'uid': urlsafe_base64_encode(force_bytes(user['username'])),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[user['email']]
    )
    email.send()
    print('celery Done')

