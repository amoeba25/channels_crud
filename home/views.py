from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    '''calls all the pizzas and orders and showcases
    them on the homepage'''
    pizza = Pizza.objects.all()
    orders = Order.objects.filter(user = request.user)
    context = {'pizza' : pizza , 'orders' : orders}
    return render(request, 'index.html', context)

def order(request , order_id):
    '''viewing the order progress with sockets'''
    order = Order.objects.filter(order_id=order_id).first()
    if order is None:
        return redirect('/')
    
    context = {'order' : order}
    return render(request , 'order.html', context)
    
    
# using this decorator, we wont have to deal with the csrf token    
@csrf_exempt
def order_pizza(request):
    user = request.user # getting the user 
    data = json.loads(request.body) # getting the body of the json response posted from the front-end
    
    # getting pizza object
    try:
        pizza =  Pizza.objects.get(id=data.get('id'))
        order = Order(user=user, pizza=pizza , amount = pizza.price)
        order.save() # saving to the datbase
        return JsonResponse({'message': 'Success'})
        
    except Pizza.DoesNotExist:
        return JsonResponse({'error': 'Something went wrong'})
    
    