from django.shortcuts import redirect, render # type: ignore
from Cart.models import Product, CartItem
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    response = render(request, "cart/index.html", {'products':products})
    return response

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity == 1:
        cart_item.delete()
    else: 
        cart_item.quantity-=1
        cart_item.save()
    return redirect('cart:view_cart')

# Define a view function for the login page 
def login_page (request): 
    # Check if the HTTP request method is POST (form submission) 
    if request.method == "POST": 
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        #Check if a user with the provided username exists 
        if not User.objects.filter(username=username).exists(): 
            # Display an error message if the username does not exist 
            messages.error(request, 'Invalid Username') 
            return redirect('/login/') 
        
        # Authenticate the user with the provided username and password user authenticate(username username, password=password) 
        user = authenticate(username=username, password=password)
        
        if user is None: 
            # Display an error message if authentication fails (invalid password) 
            messages.error(request, "Invalid Password") 
            return redirect('/login/') 
        else: 
            #Log in the user and redirect to the home page upon successful login login(request, user)
            login(request, user)
            return redirect('cart:product_list')
    
    #return the login page template(Get request)
    return render(request, 'cart/login.html')

# Define a view function for the registration page 
def register_page(request): 
    #Check if the HTTP request method is POST (form submission) 
    if request.method == 'POST': 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        # Check if a user with the provided username already exists 
        user = User.objects.filter(username=username) 

        if user.exists(): 
            #Display an information message if the username is taken 
            messages.info(request, "Username already taken!") 
            return redirect('/register/')
        # Create a new User object with the provided information 
        user = User.objects.create_user( 
            first_name=first_name, 
            last_name=last_name, 
            username=username 
        )

        # Set the user's password and save the user object 
        user.set_password (password) 
        user.save() 
        # Display an information message indicating successful account creation 
        messages.info (request, "Account created Successfully!") 
        return redirect('/register/')
    
    #Render the registration page template (Get request)
    return render(request, 'cart/register.html')

def signout(request):
    logout(request)
    return redirect('/login/')