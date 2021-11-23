# import os
# from twilio.rest import Client

# account_sid = 'AC8d1ed90c743abe70963aa42514c5587d'
# auth_token = '9cc56d0c79c60ce2ffa31d1ba8070990'
# client = Client(account_sid,auth_token)
# def send_sms(to_):
    
    
#     service = client.verify.services.create(
#                                      friendly_name='My First Verify Service'
#                                )
#     verification = client.verify \
#                      .services(service.sid) \
#                      .verifications \
#                      .create(to='+91'+str(to_), channel='sms')

#     return verification.sid
# def verify(otp,to_,sid):
#     verification_check = client.verify \
#                            .services(sid) \
#                            .verification_checks \
#                            .create(to='+91'+str(to_), code=otp)
#     return verification_check.status