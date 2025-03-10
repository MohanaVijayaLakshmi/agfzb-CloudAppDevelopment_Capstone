from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request 
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        user_exist = False
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['psw']
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # <HINT> Login the user and 
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://mohanalakshm-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        
        context = {}
        # context["dealerships"] = dealerships
        context = {"dealership_list": dealerships}
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://mohanalakshm-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(dealer_url, id = id)
        context['dealer'] = dealer

        review_url = "https://mohanalakshm-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id = id)
        for review in reviews:
            print ("sentiment", review.sentiment)
        print("REVIEWS:", reviews)
        context['reviews'] = reviews

        logger.info('Dealer ID: '+ str(dealer.id))
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, id):
    context = {}
    url = "https://mohanalakshm-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
    dealer = get_dealer_by_id_from_cf(url, id=id)
    context["dealer"] = dealer

    if request.method == 'GET':
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            review_post_url = "https://mohanalakshm-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            review = {
                "id":id,
                "time":datetime.utcnow().isoformat(),
                "name":request.user.username,  # Assuming you want to use the authenticated user's name
                "dealership" :id,                
                "review": request.POST["content"],  # Extract the review from the POST request
                "purchase": True,  # Extract purchase info from POST
                "purchase_date":request.POST["purchasedate"],  # Extract purchase date from POST
                "car_make": car.make.name,  # Extract car make from POST
                "car_model": car.name,  # Extract car model from POST
                "car_year": int(car.year.strftime("%Y")),  # Extract car year from POST
            }
            review=json.dumps(review,default=str)
            print("\nReview before new payload: ",review)
            new_payload1 = {}
            new_payload1["review"] = review
            print("\nREVIEW123:")
            post_request(review_post_url, review, id = id)
        return redirect("djangoapp:dealer_details", id = id)
