import jwt
import time
from .models import Tokens, Customers
from .customers_serialize import TokenSerialzier

def encode(**kwargs):
    #Generate epoch time and set expiration time as 5 mins after
    expiration_time = int(time.time()) + 1800
    error_msg = ''
    key = 'nuCamp202@'
    kwargs['expire_time'] = expiration_time
    token = jwt.encode(kwargs, key, algorithm="HS256")
    kwargs['token'] = token
    # print(kwargs)

    token_serializer = TokenSerialzier(data=kwargs)
    # print(token_serializer.is_valid())

    if token_serializer.is_valid():
        token_serializer.save()

    return error_msg, token

def authentication(request):
    try:
        if 'Authorization' in request.headers and verify_token(request.headers['Authorization']):
            return True
        else:
            return False
    except:
        return False

def verify_token(token, mode='chk_active'):
    key = 'nuCamp202@'

    try:
        orig_payload = jwt.decode(token, key, algorithms="HS256")
    except:
        return False

    if mode == 'chk_active':
        current_time = int(time.time())
        if current_time - orig_payload['expire_time'] < 0 and orig_payload['type'] == 'customer':
            return True
        return False
    
    if mode == 'get_id':
        return int(orig_payload['customers'])


    
