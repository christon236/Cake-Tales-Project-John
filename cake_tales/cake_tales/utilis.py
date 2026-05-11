import random

import string

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.conf import settings

from cakes.models import Order


def generate_password():

    password = ''.join(random.choices(string.ascii_letters+string.digits,k=8))

    return password


def send_email(subject,recipient,template,context):

    email_obj = EmailMultiAlternatives(subject,from_email=settings.EMAIL_HOST_USER,to={recipient})

    content = render_to_string(template,context)

    email_obj.attach_alternative(content,'text/html')

    email_obj.send()



def generate_otp():

    otp = ''.join(random.choices(string.digits,k=4))

    return otp


def generate_order_id():

    while True :

        order_id = 'CT-'+''.join(random.choices(string.digits,k=7))

        if not Order.objects.filter(order_id=order_id).exists():

            return order_id



