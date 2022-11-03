from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from . models import *
from . forms import CheckoutForm
from django.core.paginator import Paginator
from django.contrib import messages

from django.db.models import Q
from django.conf import settings
# Create your views here.
def index(request):
    # just loader
    return render(request, 'stores/index.html')

    
def home(request):
    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        totalnum = cart.cartproduct_set.all().count()
    else:
        cart = Cart.objects.all()
        totalnum = cart.count()

    
    # banner
    banner = Banner.objects.all()
    # products
    products = Product.objects.all()
    # paginator
    pagination = Paginator(products,3)
    page_number = request.GET.get('page')
    car_list = pagination.get_page(page_number)
    context={
        'banner':banner,
        'products':products,
        'paginator': car_list,
        'carts':totalnum
    }

    return render(request, 'stores/home.html',context)

def singleCar(request,id):
    product = Product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request, 'stores/single.html',context)


def addCart(request,id):
    # get the product you want to add to cart
    cart_product = Product.objects.get(id=id)
    
    # check if cart exist
    cart_id = request.session.get('cart_id',None)

    if cart_id:
        # get the particular cart
        cart_item = Cart.objects.get(id = cart_id)
        this_product = cart_item.cartproduct_set.filter(product=cart_product)

        if this_product.exists():
            cartproduct = this_product.last()
            cartproduct.quantity +=1
            cartproduct.subtotal += cart_product.price
            cartproduct.save()
            cart_item.total += cart_product.price
            cart_item.save()
        else:
            cartproduct  = CartProduct.objects.create(cart=cart_item,product=cart_product,quantity=1,rate=cart_product.price,subtotal=cart_product.price)
            cart_item.total += cart_product.price
            cart_item.save()

    else:
        cart_item = Cart.objects.create(total=0)
        request.session['cart_id'] = cart_item.id
        cartproduct  = CartProduct.objects.create(cart=cart_item,product=cart_product,quantity=1,rate=cart_product.price,subtotal=cart_product.price)
        cart_item.total += cart_product.price
        cart_item.save()

    return redirect('home')

def myCart(request):

    # session
    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)

        # logged in user
        if request.user.is_authenticated and request.user.customer:
            cart_item.customer = request.user.customer
            cart_item.save()
    else:
        cart_item = None


    context={
        'cart':cart_item
    }
    return render(request, 'stores/mycart.html',context)


def manageCart(request,id):
    action = request.GET.get('action')
    cart_obj = CartProduct.objects.get(id=id)
    cart = cart_obj.cart


    if action == 'inc':
        cart_obj.quantity +=1
        cart_obj.subtotal += cart_obj.rate
        cart_obj.save()
        cart.total += cart_obj.rate
        cart.save()
        messages.success(request, 'Item increased in cart')
    elif action == 'dcr':
        cart_obj.quantity -=1
        cart_obj.subtotal -= cart_obj.rate
        cart_obj.save()
        cart.total -= cart_obj.rate
        cart.save()
        messages.success(request, 'Item decreased in cart')

        if cart_obj.quantity == 0:
            cart_obj.delete()

    elif action == 'rmv':
        cart.total -= cart_obj.subtotal
        cart.save()
        cart_obj.delete()
        messages.success(request, 'Item removed in cart')
    else:
        pass

    return redirect('myCart')

def checkout(request):
    cart_id = request.session.get('cart_id',None)
    cart_obj = Cart.objects.get(id=cart_id)
    form = CheckoutForm()

    if request.user.is_authenticated and request.user.customer:
        pass
    else:
        return redirect('/users/login/?next=/checkout/')

    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit= False)
            form.cart = cart_obj
            form.amount = cart_obj.total
            form.subtotal = cart_obj.total
            form.discount = 0
            form.order_status = 'Order Received'
            payments = form.payment_method
            del request.session['cart_id']
            payments = form.payment_method
            form.save()

            order = form.id
            if payments == 'Paystack':
                return redirect('payments', id =order)


    context = {
        'form':form,
        'cart':cart_obj
    }
    return render(request, 'stores/checkout.html',context)

def payments(request, id):
    orders = Order.objects.get(id=id)

    context ={
    'order':orders,
    'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request,'stores/payment.html',context)

def verify_payment(request:HttpRequest,ref:str) -> HttpResponse:
    payment = get_object_or_404(Order, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.success(request, 'Verification Failed')
    return redirect('home')

def search(request):
    if request.method == 'GET':
        kw = request.GET.get('kword')
        search = Product.objects.filter(Q(name__icontains=kw) | Q(price__icontains=kw))

    context={
        'search':search
    }
    return render(request, 'stores/search.html',context)

def clearCart(request):
    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart.cartproduct_set.all().delete()
        cart.total = 0
        cart.save()
    return redirect('myCart')
