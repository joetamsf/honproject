import os
import subprocess
import requests
import time
import psutil

test_url = 'http://localhost:8000'

def clean_up():
    file = 'db.sqlite3'
    if os.path.exists(os.path.abspath(file)):
        os.remove(os.path.abspath(file))

def end_process(pid):
    parent = psutil.Process(pid)
    for c in parent.children(recursive=True):
        c.kill()

def login_test():
    r = requests.get(test_url + '/customers/login', data = {'username': 'user01', 'password':'password01'})
    # print(r.json())
    if 'Token' in r.json():
        return r.json()['Token']

    return False

def create_order(token):
    header = {'Authorization': token}
    r = requests.post(test_url + '/customers/new_order', data = {'orders': [4]}, headers=header)
    print(r.json())
    if 'Order_id' in r.json():
        return r.json()['Order_id']

    return False

def check_order(token, oid):
    header = {'Authorization': token}
    r = requests.get(test_url + '/customers/my_orders', headers=header)

    if 'order_detail_1' in r.json():
        if 'order_id' in r.json()['order_detail_1']:
            if oid == r.json()['order_detail_1']['order_id']:
                return True

    return False

def main():
    copy_env = os.environ.copy()
    copy_env['Mode'] = 'test'

    proc1 = subprocess.Popen(["python", "manage.py", "migrate"], env=copy_env)
    proc1.wait()

    proc2 = subprocess.Popen(["python", "test_data.py"], env=copy_env)
    proc2.wait()

    proc3 = subprocess.Popen(["python", "manage.py", "runserver", "0.0.0.0:8000"], env=copy_env)
    time.sleep(5)

    token = login_test()

    try:
        if not token == False:
            oid = create_order(token)
        else:
            print("Testing failed at Login Stage")
            end_process(proc3.pid)
            proc3.kill()
    except:
        end_process(proc3.pid)
        proc3.kill()

    try:
        if not oid == False:
            if check_order(token, oid):
                print("All tests successfully completed")
            else:
                print("Testing failed on check order")
                end_process(proc3.pid)
                proc3.kill()
        else:
            print("Testing failed on create order")
            end_process(proc3.pid)
            proc3.kill()
    except:
        end_process(proc3.pid)
        proc3.kill()

    end_process(proc3.pid)
    proc3.kill() 

    

if __name__ == '__main__':
    clean_up()
    main()
    clean_up()




