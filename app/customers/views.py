from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# from app.staffs.staff_token_generator import authentication
from .models import Customers
from rest_framework.decorators import api_view
from .customer_token_generator import encode, verify_token, authentication
from .customer_usage_msg import show_add_order_usage, show_add_new_account
from orders.models import Orders, Foods

# Create your views here.
# def generate_token(username, cid):

@api_view(['GET'])
def customer_login(request):
    if request.data and 'username' in request.data and 'password' in request.data:
        cid = Customers.objects.values_list('id').filter(username=request.data['username'], password=request.data['password'])
        if len(cid) > 0: 
            error_msg, c_token = encode(customers = cid[0][0], type = 'customer')
            if error_msg:
                return JsonResponse({'error_msg': error_msg})
            else:
                return JsonResponse({'msg':'You have successfully Logged in',  
                                     'Token': c_token})

    return JsonResponse({'error_msg': 'login failed'})

@api_view(['GET'])
def validate_token(request):
    if request.headers['Authorization'] and verify_token(request.headers['Authorization']):
        return HttpResponse('Your token is still valid')

    return HttpResponse('Your token is expired or Authorization header is missing, please login again')

@api_view(['POST'])
def create_account(request):
    mandatory_items = ['username','firstname','lastname','password','address','phone']

    for i in mandatory_items:
        if i in request.data:
            if request.data[i] == '':
                return JsonResponse({'error_msg': 'field '+str(i)+ ' cannot be empty'})
            else:
                continue
        return JsonResponse(show_add_new_account(),safe=False)

    try:
        if len(Customers.objects.filter(username=request.data['username'])) == 0:
            c = Customers(username=request.data['username'],
                    firstname = request.data['firstname'],
                    lastname = request.data['lastname'],
                    password = request.data['password'],
                    address = request.data['address'],
                    phone = request.data['phone']
                )
            c.save()
            return JsonResponse({'msg': 'Account created'})
    except:
        return JsonResponse({'msg': 'Failed to create account'}) 
    
    return JsonResponse({'msg': 'Please set another username'})

@api_view(['POST'])
def create_order(request):
    uid = ''
    succeed_items = []

    if not authentication(request):
        return JsonResponse({'error_msg': 'You are not authorized to access this page',
                             'solution': 'Logged into the system and set Authorization header'})

    uid = verify_token(request.headers['Authorization'],'get_id')
    
    # return JsonResponse({'error_msg': 'Your token is expired or Authorization header is missing, please login again'})

    if not 'orders' in request.data or not len(request.data['orders']) > 0:
        return JsonResponse(show_add_order_usage(),safe=False)
    
    #Prepare data for eliminating duplicated item and non exist item
    if len(request.data['orders']) > len(set(request.data['orders'])):
        return JsonResponse({'error_msg': 'duplicated item is not allowed'})

    #Insert customers ID into Orders table
    o = Orders(customers=Customers.objects.get(id=uid))
    o.save()

    for _ in range(len(request.data['orders'])):
        fid = request.data['orders'][_]
        
        if fid not in range(1,6):
            continue

        o.food.add(Foods.objects.get(id=fid))
        succeed_items.append(fid)
            
    return JsonResponse({'Status': "Successful",'Order_id': o.id, 'items': succeed_items}, safe=False)

@api_view(['GET'])
def get_my_order(request):
    try:
        if authentication(request):
            uid = verify_token(request.headers['Authorization'],'get_id')
            myorder = Orders.objects.filter(customers=uid)
        else:
            return JsonResponse({'error_msg': 'You are not authorized to access this page',
                             'solution': 'Logged into the system and set Authorization header'})
    except:
        return JsonResponse({'error_msg': 'Your token is expired or Authorization header is missing, please login again'})


    if not len(myorder) > 0:
        return JsonResponse({'msg': 'Currently you dont have any orders'})
    
    myorder_dict = {}
        
    for _ in range(len(myorder)): 
        oid = myorder[_].id
        food_list = []
        temp_dict = {}
        temp_dict['order_id'] = oid
        temp_dict['order_date'] = myorder[_].order_date 
        food_items = Foods.objects.filter(orders__id=oid)
        
        for foods in food_items:
            food_list.append(foods.name)
        
        temp_dict['items'] = food_list
        myorder_dict['order_detail_'+str(_+1)] = temp_dict

    return JsonResponse(myorder_dict)

@api_view(['DELETE'])
def delete_my_order(request):
    try:
        if authentication(request):
            uid = verify_token(request.headers['Authorization'],'get_id')
            if 'order_id' in request.data:
                o = Orders.objects.get(id=request.data['order_id'],customers=uid)
                if len(o.staffs.values('id')) == 0:
                    o.delete()
                    return JsonResponse({'msg': 'Your order has been cancelled'})
                else:
                    return JsonResponse({'error_msg': 'You cannot cancel an order as it is being prepared'})

        return JsonResponse({'error_msg': 'Your token is expired or Authorization header is missing, please login again'})
    except Exception as e:   
        print(e)      
        return JsonResponse({'error_msg': 'Unexpected Error'})

@api_view(['POST'])
def update_password(request):
    try:
        if authentication(request):
            if 'password' in request.data:
                uid = verify_token(request.headers['Authorization'],'get_id')
                c = Customers.objects.get(id=uid)
                c.password = request.data['password']
                c.save()
                return JsonResponse({'msg': 'Your password has been updated'})
            else:
                return JsonResponse({'error_msg': 'missing password field in request json'})
    except:
        return JsonResponse({'error_msg': 'Failed to update your password'})

    return JsonResponse({'error_msg': 'missing password field in request json'})

    

