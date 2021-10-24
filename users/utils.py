from django.db import models
import os
from twilio.rest import Client

# coding: utf-8
from decouple import Csv, config
from dj_database_url import parse as db_url


def sms_send(to_phone, code):

    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    sender_phone_num = config('SENDER_PHONE_NUMBER')      
    receiver_phone_num = to_phone
    
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Welcome! Your verififation code is: "+str(code),
                        from_=sender_phone_num,
                        to=receiver_phone_num,
                    )

    print(message.sid)