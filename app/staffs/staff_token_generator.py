import jwt
import time

def encode(**kwargs):
    #Generate epoch time and set expiration time as 30 mins after
    expiration_time = int(time.time()) + 1800
    key = 'nuCamp202@'
    kwargs['expire_time'] = expiration_time
    token = jwt.encode(kwargs, key, algorithm="HS256")

    return token

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
        if current_time - orig_payload['expire_time'] < 0:
            if orig_payload['type'] == 'staff':
                return True
        return False
    
    if mode == 'get_id':
        return int(orig_payload['id'])
    
def is_manager(request):
    try:
        if authentication(request):
            key = 'nuCamp202@'
            orig_payload = jwt.decode(request.headers['Authorization'], key, algorithms="HS256")
            if orig_payload['role'] == 'manager':
                print(orig_payload)
                return True
    except Exception as e:
        print(e)
        return False

    


    
