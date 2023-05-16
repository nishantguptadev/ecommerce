from django.shortcuts import render, redirect
from .models import *
from math import ceil
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your views here.
# def totalitem():
#     totalitem = 0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
         

def index(request):
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        
        nSlides = n// 4 + ceil((n/4)- (n//4))
        allProds.append([prod, range(1,nSlides), nSlides])
    params={
        'allProds':allProds,
    }
    return render(request, "ecomapp/index.html", params)
    # electronics = Product.objects.filter(category="Electronics")
    # return render(request, "ecomapp/index.html", {'electronics':electronics})

def product_detail(request, pk):
    product=Product.objects.get(pk=pk)
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/productdetail.html", {'product':product,'like':like})
    else:
        return render(request, "ecomapp/productdetail.html", {'product': product})
    

def buy_now(request):
    if request.user.is_authenticated:
        user= request.user
        product_id=request.GET.get('prod_id')
        product = Product.objects.get(id=product_id) #to get instance of product from Product table through id
        cart_prodcut = Cart.objects.filter(product=product).filter(user=user)
        Cart(user=user, product=product).save() #save user and product in cart
        return redirect('/checkout') # this url will send/redirect to show_cart function below
    else:
        messages.info(request, "Please signin to add items to your cart!!")
        return render(request, "eauth/signin.html")


def cosmetics(request):
    cat=Product.objects.filter(category='Cosmetics')
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/cosmetics.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/cosmetics.html", {'cat':cat})

def electronic(request, data=None):
    # brand=Product.objects.filter(category='Electronics').values("brand").distinct()
    if data == None:
        cat = Product.objects.filter(category='Electronics')
    elif data == 'below':
        cat = Product.objects.filter(category='Electronics').filter(discounted_price__lt=30000)#lt is lessthan
    elif data == 'above':
        cat = Product.objects.filter(category='Electronics').filter(discounted_price__gt=30000)# gt is greater then
    elif data == 'Camera' or 'Mobile' or 'Laptop':
        cat = Product.objects.filter(category='Electronics').filter(sub_category=data)
       
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/electronic.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/electronic.html", {'cat':cat})

def mobiles(request, data=None):
    # brand=Product.objects.filter(category='Electronics').values("brand").distinct()
    if data == None:
        cat = Product.objects.filter(sub_category='Mobile')
    elif data == 'below':
        cat = Product.objects.filter(sub_category='Mobile').filter(discounted_price__lt=20000)
    elif data == 'above':
        cat = Product.objects.filter(sub_category='Mobile').filter(discounted_price__gt=20000)# gt is greater then 
    elif data == 'Samsung' or 'Apple' or 'OnePlus' or 'Redmi':
        cat = Product.objects.filter(sub_category='Mobile').filter(brand=data)
      
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/mobiles.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/mobiles.html", {'cat':cat})

def topwear(request, data=None):
    # brand=Product.objects.filter(category='Electronics').values("brand").distinct()
    if data == None:
        cat = Product.objects.filter(sub_category='Topwear')
    elif data == 'below':
        cat = Product.objects.filter(sub_category='Topwear').filter(discounted_price__lt=500)
    elif data == 'above':
        cat = Product.objects.filter(sub_category='Topwear').filter(discounted_price__gt=500)# gt is greater then 
      
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/topwear.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/topwear.html", {'cat':cat})

def bottomwear(request, data=None):
    # brand=Product.objects.filter(category='Electronics').values("brand").distinct()
    if data == None:
        cat = Product.objects.filter(sub_category='Bottomwear')
    elif data == 'below':
        cat = Product.objects.filter(sub_category='Bottomwear').filter(discounted_price__lt=500)
    elif data == 'above':
        cat = Product.objects.filter(sub_category='Bottomwear').filter(discounted_price__gt=500)# gt is greater then    
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/bottomwear.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/bottomwear.html", {'cat':cat})

def laptops(request, data=None):
    # brand=Product.objects.filter(category='Electronics').values("brand").distinct()
    if data == None:
        cat = Product.objects.filter(sub_category='Laptop')
    elif data == 'below':
        cat = Product.objects.filter(sub_category='Laptop').filter(discounted_price__lt=35000)
    elif data == 'above':
        cat = Product.objects.filter(sub_category='Laptop').filter(discounted_price__gt=35000)# gt is greater then
    elif data == 'HP' or 'Lenovo' or 'Samsung':
        cat = Product.objects.filter(sub_category='Laptop').filter(brand=data)
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/laptops.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/laptops.html", {'cat':cat})
   

def fashion(request, data=None):
    if data == None:
        cat = Product.objects.filter(category='Fashion')
    elif data == 'below':
        cat = Product.objects.filter(category='Fashion').filter(discounted_price__lt=500)
    elif data == 'above':
        cat = Product.objects.filter(category='Fashion').filter(discounted_price__gt=500)
    elif data == 'Topwear' or 'Bottomwear':
        cat = Product.objects.filter(category='Fashion').filter(sub_category=data)
    
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/fashion.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/fashion.html", {'cat':cat})


def jewellery(request, data=None):
    if data == None:
        cat = Product.objects.filter(category='Jewellery')
    elif data == 'below':
        cat = Product.objects.filter(category='Jewellery').filter(discounted_price__lt=50000)
    elif data == 'above':
        cat = Product.objects.filter(category='Jewellery').filter(discounted_price__gt=50000)
    elif data == 'Necklace' or 'Earings' or 'Bangles':
        cat = Product.objects.filter(category='Jewellery').filter(sub_category=data)
    
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/jewellery.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/jewellery.html", {'cat':cat})

def watches(request, data=None):
    if data == None:
        cat = Product.objects.filter(category='Watch')
    elif data == 'below':
        cat = Product.objects.filter(category='Watch').filter(discounted_price__lt=1000)
    elif data == 'above':
        cat = Product.objects.filter(category='Watch').filter(discounted_price__gt=1000)
    elif data == 'Titan' or 'Fastrack':
        cat = Product.objects.filter(category='Watch').filter(brand=data)
    
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/watches.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/watches.html", {'cat':cat})

def add_to_cart(request):
    if request.user.is_authenticated:
        user= request.user
        product_id=request.GET.get('prod_id')
        product = Product.objects.get(id=product_id) #to get instance of product from Product table through id
        cart_prodcut = Cart.objects.filter(product=product).filter(user=user)
        if cart_prodcut:
            messages.warning(request, "This Product is already in your cart")
            return redirect('/cart')
        else:
            Cart(user=user, product=product).save() #save user and product in cart
            return redirect('/cart') # this url will send/redirect to show_cart function below
    else:
        messages.info(request, "Please signin to add items to your cart!!")
        return render(request, "eauth/signin.html")

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user) # it will give query set of id in cart table for particular user
        coupon = Coupon.objects.all()
        appliedcoupon=""
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_prodcut = [p for p in Cart.objects.all() if p.user == user] # it will give list of id in cart table for particular user
        # print(cart)
        # print(cart_prodcut)
        if cart_prodcut:
            for p in cart_prodcut:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount=amount + shipping_amount

            if request.method=="POST":
                appliedcoupon=request.POST.get('coupon','')
                coupon=Coupon.objects.all()
                for i in coupon:
                    if i.name == appliedcoupon:
                        coupon_type=Coupon.objects.get(name=i.name)
                        discount_type=coupon_type.discount_type
                        discount=int(coupon_type.discount)
                        if discount_type == "Cash":
                            amount=amount-discount
                            total_amount=amount + shipping_amount
                        else:
                            discount=(discount/100)*amount
                            amount=amount-discount
                            total_amount=amount + shipping_amount
                        messages.info(request, "Your Coupon has been applied!!")
                    
            return render(request, 'ecomapp/addtocart.html', {'carts':cart,'amount':amount, 'total_amount': total_amount, 'coupon': coupon, 'appliedcoupon':appliedcoupon})
        else:
            messages.info(request, "Your Cart is Empty! Please add some items in your cart!!")
            return render(request, 'ecomapp/emptycart.html')
    else:
        return render(request, 'eauth/signin.html')

def pluscart(request):
    if request.method == 'GET':
        prod_id=request.GET.get('product_id') # this product_id is used in js to store product id
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_prodcut = [p for p in Cart.objects.all() if p.user == request.user] # it will give list of id in cart table for particular user
        for p in cart_prodcut:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount=amount + shipping_amount
        
        data= {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount,
            
        }
        return JsonResponse(data)

def minuscart(request):
    if request.method == 'GET':
        prod_id=request.GET.get('product_id') # this product_id is used in js to store product id
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_prodcut = [p for p in Cart.objects.all() if p.user == request.user] # it will give list of id in cart table for particular user
        for p in cart_prodcut:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount=amount + shipping_amount
        
        data= {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount,
            
        }
        return JsonResponse(data)

def removecart(request):
    if request.method == 'GET':
        prod_id=request.GET.get('product_id') # this product_id is used in js to store product id
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_prodcut = [p for p in Cart.objects.all() if p.user == request.user] # it will give list of id in cart table for particular user
        for p in cart_prodcut:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount=amount + shipping_amount
        
        data= {
            'amount': amount,
            'total_amount': total_amount,
            
        }
        return JsonResponse(data)

def itemadded(request):
    if request.method == 'GET':
        user= request.user
        product_id=request.GET.get('prod_id')
        product = Product.objects.get(id=product_id) #to get instance of product from Product table through id
        cart_product = Cart.objects.filter(product=product).filter(user=user)
        data= {
            'itemadded': "itemadded",
            }
        if cart_product:
            messages.warning(request, "This Product is already in your cart")
            return JsonResponse(data)
        else:
            Cart(user=user, product=product).save() #save user and product in cart
            return JsonResponse(data)

def checkout(request):
    totalamount=0.0
    if request.method=="POST":
        print("hello")
        totalamount=request.POST.get("total_amount")
    else:
        amount=0.0
        shipping_amount=70.0
        cart_prodcut = [p for p in Cart.objects.all() if p.user == request.user] # it will give list of id in cart table for particular user
        if cart_prodcut:
            for p in cart_prodcut:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount=amount + shipping_amount

    user=request.user
    address = Customer.objects.filter(user=user)
    items = Cart.objects.filter(user=user)
      
    return render(request, 'ecomapp/checkout.html', {'address':address, 'items':items, 'totalamount':totalamount})

def payment(request):
    user = request.user
    custid = request.GET.get('custid')
    if custid!=None:
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for i in cart:
            OrderPlaced(user=user, customer=customer, product=i.product, quantity=i.quantity).save()
            i.delete()
        messages.info(request, "Your order have been placed. Thanks for ordering with us!!")
        return redirect("orders")
    else:
        messages.info(request,'please select the address')
        return redirect("checkout")

def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user)
    if orders:
        return render(request, "ecomapp/orders.html", {'orders':orders})
    else:
        messages.info(request, "You haven't placed any order yet!!")
        return render(request, "ecomapp/orders.html")
        
def cancelorder(request, pk):
    user = request.user
    canceled='Canceled'
    if pk!=None:
        # product = Orderplaced.objects.get(id=pk)
        i = OrderPlaced.objects.get(id=pk)
        OrderPlaced(user=user, customer=i.customer, product=i.product, quantity=i.quantity, status=canceled).save()
        i.delete()
        return redirect("/orders")

def search(request):
    query= request.GET.get('q')
    search=Product.objects.filter(Q(category__icontains=query) | Q(sub_category__icontains=query) | Q(description__icontains=query)| Q(title__icontains=query) | Q(brand__icontains=query))
    print(search)
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/search.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/search.html", {'cat':cat})

def aboutus(request):
    return render(request, "ecomapp/aboutus.html")

def terms(request):
    return render(request, "ecomapp/terms.html")

def customer(request):
    if request.method=='POST':
        user=request.POST.get('user','')
        email=request.POST.get('email', '')
        query=request.POST.get('query', '')
        detail=request.POST.get('detail', '')
        service=CustomerService(user=user, email=email, query=query, detail=detail)
        service.save()
        messages.success(request, "We will get back to you soon....Thanks for contacting us.")
        return render(request, 'ecomapp/customer.html')
    return render(request, 'ecomapp/customer.html')

def address(request):
    if request.method=='POST':
        user=request.user
        name=request.POST.get('name', '')
        locality=request.POST.get('address', '') 
        address = request.POST.get('address2', '')
        city=request.POST.get('city', '')
        zipcode=request.POST.get('zipcode', '')
        state=request.POST.get('state', '')
        address=Customer(user=user, name=name, locality=locality,address=address, city=city, zipcode=zipcode, state=state)
        address.save()
        return redirect('/profile')
    return render(request, 'ecomapp/address.html')

def deladd(request, pk):
    deladd=Customer.objects.get(id=pk)
    deladd.delete()
    return redirect('/profile')

def editadd(request, pk):
    user=request.user
    editadd=Customer.objects.get(id=pk)
    if request.method=='POST':
        user=request.user
        name=request.POST.get('name', '')
        locality=request.POST.get('address', '') 
        address = request.POST.get('address2', '')
        city=request.POST.get('city', '')
        zipcode=request.POST.get('zipcode', '')
        state=request.POST.get('state', '')
        address=Customer(user=user, name=name, locality=locality,address=address, city=city, zipcode=zipcode, state=state)
        address.save()
        editadd.delete()
        return redirect('/profile')

    return render(request, 'ecomapp/editadd.html',{'editadd':editadd})


def profile(request):
    user=request.user
    if user.is_anonymous:
        return render(request, "eauth/signin.html")
    else:
        cat = Customer.objects.filter(user=user)
        return render(request, "ecomapp/profile.html", {'cat':cat})

def newadd(request, data=None):
    if data == None:
        cat = Product.objects.all().order_by('-id')[:9]
    
    elif data == 'Electronics' or 'Jewellery' or 'Watch' or 'Cosmetics' or 'Fashion':
        cat = Product.objects.filter(category=data).order_by('-id')[:9]
       
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/newadd.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/newadd.html", {'cat':cat})
    
def bestsell(request):
    cat = OrderPlaced.objects.all().order_by('-id')[:6]
    user=request.user
    if user.is_authenticated:
        like=Like.objects.all().filter(user=request.user)
        return render(request, "ecomapp/bestsell.html", {'cat':cat,'like':like})
    else:
        return render(request, "ecomapp/bestsell.html", {'cat':cat})

# def like_now(request):
#     status=False
#     if request.user.is_authenticated:
#         user= request.user
#         product_id=request.GET.get('prod_id')
#         product = Product.objects.get(id=product_id) #to get instance of product from Product table through id
#         status=True
#         cart_prodcut = Like.objects.filter(product=product).filter(user=user)
#         Like(user=user, product=product, status=status).save() #save user and product in cart
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))#to return to the same page

def wishlist(request):
    user=request.user
    if user.is_authenticated:
        cat = Like.objects.filter(user=user)
        if cat:
            like=Like.objects.all().filter(user=request.user)
            return render(request, "ecomapp/wishlist.html", {'cat':cat,'like':like})
        else:
            messages.info(request, "You haven't liked anything yet")
        return render(request, "ecomapp/wishlist.html")        
    else:
        return render(request, "eauth/signin.html")

def add_to_wishlist(request): #this function is used to delete also
    product_id = request.GET.get("id")
    product = Product.objects.get(id=product_id)
    context = {}
    wishlist_count = Like.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)
    if wishlist_count > 0:
        now_wishlist=Like.objects.filter(product=product, user=request.user).delete()
        context = {
            "bool": False
        }

    else:
        now_wishlist=Like.objects.create(
            product=product,
            user=request.user,
            status=True
        )
    
        context= {
            "bool": True
         }

    return JsonResponse(context)

    
    
        
