from django.shortcuts import render
# from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from staffs.models import Staffs
from staffs.staff_serialize import StaffSerializer
from staffs.usage_msg import show_add_staff_usage
from orders.models import Orders, Foods
from customers.models import Customers
from .staff_token_generator import encode, is_manager, verify_token, authentication

# Create your views here.

def staffs_index(request):
    context = {
        'message': 'first msg',
        'content': 'test msg001',
    }

    print(request.body)
    return render(request, "home.html", context)

@api_view(['GET'])
def staff_login(request):
    #check request data for id and password field
    if not 'id' in request.data or not 'password' in request.data:
        return JsonResponse({'error_msg': 'missing id or password'})

    # Using the id and password to query database 
    try:
        login = Staffs.objects.get(id=request.data['id'], password=request.data['password'])

        token = encode(id = login.id, role = login.role, type = 'staff')
        return JsonResponse({'msg': 'You have successfully logged in. ',
                             'token': token})
    except Exception as e:
        print(e)
        return JsonResponse({'error_msg': 'Invalid ID or Password'})

@api_view(['GET'])
def show_all_staffs(request):

    try:
        if not is_manager(request):
                return JsonResponse({'error_msg': 'You are not authorized to access this page'})
    except:
        return JsonResponse({'error_msg': 'Missing Authorization header or Authentication failed'})

    staff_list = []
    staffslist = Staffs.objects.values('id','firstname','lastname', 'staff_type')

    for i in range(len(staffslist)):
        staff_type = ''
        if staffslist[i]['staff_type'] == 'ft':
            staff_type = 'Full Time'
        else:
            staff_type = 'Part Time'
        staff_list.append({
            'id': str(staffslist[i]['id']), 
            'firstname': staffslist[i]['firstname'],
            'lastname': staffslist[i]['lastname'],
            'staff_type': staff_type
            }) 
        
    response_all_staff = JsonResponse(staff_list, safe=False)

    return response_all_staff

@api_view(['POST'])
def add_new_staff(request):
    if is_manager(request):
        if request.data:
            staff_serialize = StaffSerializer(data=request.data)
            if staff_serialize.is_valid():
                if len(Staffs.objects.filter(ssn=request.data['ssn'])) == 0:
                    staff_serialize.save()
                    sid = Staffs.objects.values('id').filter(ssn=request.data['ssn'])[0]['id']
                    return JsonResponse({'id': sid})
    else:
        return JsonResponse({'error_msg': 'You are not authorized to access this page'})
            
    return JsonResponse(show_add_staff_usage(), safe=False)

@api_view(['GET'])
def get_all_orders(request):

    if not authentication(request):
        return JsonResponse({'error_msg': 'You are not authorized to access this page'})

    #First select all records from orders,foods and customers table
    #Avoid N + 1 Problem of ORM
    all_orders = Orders.objects.all()
    all_foods = Foods.objects.all()
    all_customers = Customers.objects.all()
    all_orders_dict = {}

    for i, o in enumerate(all_orders):
        temp_dict = {}
        temp_list = []
        oid = o.id
        cid = o.customers_id
        customer_name = all_customers.filter(id=cid).values_list('firstname', 'lastname')
        customer_food = all_foods.filter(orders__id=oid)

        temp_dict['order_id'] = oid
        temp_dict['order_date'] = all_orders[i].order_date
        temp_dict['customer'] = str(customer_name[0][0]) + " " + str(customer_name[0][1])

        for f in range(len(customer_food)):
            temp_list.append(customer_food[f].name)

        temp_dict['foods'] = temp_list

        all_orders_dict['Order_detail_'+str(i+1)] = temp_dict

    return JsonResponse(all_orders_dict)

@api_view(['POST'])
def assign_order(request):
    if is_manager(request):
    # Make sure 'order_id' and 'staff_id' in the request.data
        if 'order_id' in request.data and 'staff_id' in request.data:
            if not str(request.data['order_id']).isnumeric() or not str(request.data['staff_id']).isnumeric():
                return JsonResponse({'error_msg': 'data on staff_id or order_id must an integer'})
        else:        
            return JsonResponse({'error_msg': 'missing staff_id or order_id'})
    else:
        return JsonResponse({'error_msg': 'Only manager allowed to assign staffs to an order'})


    # Test if the order_id and staff exist in order and staff table
    try:
        s = Staffs.objects.get(id=request.data['staff_id'])
        o = Orders.objects.get(id=request.data['order_id'])
        # Also make sure record of order_id + staff_id doesnt exist in cookingstaff table     
        # Add a record to cookingstaff table
        if len(o.staffs.filter(id=s.id)) == 0:
            o.staffs.add(s)   
            return JsonResponse({'msg': 'successfully added id: '+ str(s.id) + ' to order id: '+ str(o.id)})
        else:
            return JsonResponse({'error_msg': 'Assignment exists'})
    except Exception as e:
        print(e)
        return JsonResponse({'error_msg': 'failed to assign staff to order'})

@api_view(['POST'])
def update_password(request):
    if not authentication(request):
        return JsonResponse({'error_msg': 'You are not authorized to access this page'})
    
    if not 'password' in request.data:
        return JsonResponse({'error_msg': 'missing password field in request json'})
            
    try:
        sid = verify_token(request.headers['Authorization'],'get_id')
        s = Staffs.objects.get(id=sid)
        s.password = request.data['password']
        s.save()
        return JsonResponse({'msg': 'Your password has been updated'})
    except:
        return JsonResponse({'error_msg': 'Failed to update your password'})
            


        

    
    

    