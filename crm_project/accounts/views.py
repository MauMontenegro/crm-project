from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout


from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user,allowed_users,admin_only

from django.contrib.auth.models import Group    

from django.contrib.auth import views as auth_views

@unauthenticated_user
def loginPage(request):    
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        # Authenticate
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home:home')
        else:
            messages.info(request,'Username OR password is incorrect')            

    context={}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home:login')

def register(request):
    # If user is already Logged in, then he cannot go to register or login page
    if request.user.is_authenticated:
        return redirect('home:home')
    else:
        form=CreateUserForm()
        if request.method=="POST":
            form=CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username=form.cleaned_data.get('username')            

                messages.success(request,'Account was created for ' + username)
                return redirect('home:login')

    context={'form':form}
    return render(request,'accounts/register.html',context)


@login_required(login_url='home:login')
@admin_only
def home(request):
    customers=Customer.objects.all()    
    orders=Order.objects.all()

    total_customers= customers.count()
    total_orders = orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()  

    context={'orders':orders,'customers':customers,'total_orders':total_orders,'total_customers':total_customers,
             'delivered':delivered,'pending':pending}

    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='home:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{
        'products':products
        })

@login_required(login_url='home:login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)

import logging

logger = logging.getLogger(__name__)

@login_required(login_url='home:login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            # Check if a new profile picture is being uploaded
            if 'profile_pic' in request.FILES:
                logger.info(f"New profile picture uploaded: {request.FILES['profile_pic'].name}")
                # Delete the old profile picture if it exists and is not in use
                if customer.profile_pic:
                    try:
                        # Close the file if it is open
                        if hasattr(customer.profile_pic, 'close'):
                            customer.profile_pic.close()
                        # Delete the file if it exists
                        if customer.profile_pic.storage.exists(customer.profile_pic.name):
                            logger.info(f"Deleting old profile picture: {customer.profile_pic.name}")
                            customer.profile_pic.delete(save=False)
                    except Exception as e:
                        logger.error(f"Error deleting file: {e}")
                        print(f"Error deleting file: {e}")
            form.save()
            return redirect('home:account')
    else:
        form = CustomerForm(instance=customer)

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='home:login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    query=request.GET.get('query')
    query2=request.GET.get('query2')
    query3=request.GET.get('query3')
    customer= Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    total_orders=orders.count()

    if query or query2 or query3:
        c1= Q(product__name__contains=query) if query else Q()     
        c2= Q(product__category__contains=query2) if query2 else Q()
        c3= Q(status__contains=query3) if query3 else Q()
        orders=orders.filter(c1&c2&c3)

    context={'customer':customer,
             'orders':orders,
             'total_orders':total_orders,
             'query':query,
             'query2':query2,
             'query3':query3,} 

    return render(request,'accounts/customer.html',context)

@login_required(login_url='home:login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=3)  #Customer is the Father form and Orders are the childs (Multiple Orders for one Customer
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    

    # If request comes for a formulary POST
    if request.method == 'POST':
        #print('Printing POST',request.POST)
        #form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        
    # If request comes for a button in dashboard or something else
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='home:login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):    
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order) 

    if request.method == 'POST':        
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():            
            form.save()            
            return redirect('/')


    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='home:login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order= Order.objects.get(id=pk)
    form=OrderForm(instance=order) 

    if request.method== "POST":
        order.delete()
        return redirect('/')
   

    context = {'order':order,'form':form}
    return render(request,'accounts/delete.html',context)