# Uncomment the required imports before adding the code
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel, Dealership
from .populate import initiate
from django.conf import settings
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)
def get_cars(request):
    try:
        count = CarMake.objects.filter().count()
        print(f"CarMake count: {count}")
        if count == 0:
            print("Calling initiate() to populate database")
            initiate()
        car_models = CarModel.objects.select_related('car_make')
        print(f"CarModel count: {CarModel.objects.count()}")
        cars = []
        for car_model in car_models:
            cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
        return JsonResponse({"CarModels": cars})
    except Exception as e:
        print(f"Error in get_cars: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
# Update the `get_dealerships` view to render the index page with
# a list of dealerships
@csrf_exempt
def get_dealerships(request):
    try:
        dealers = Dealership.objects.all().values('id', 'name', 'address', 'city', 'state', 'zip_code', 'phone')
        print(f"Found {len(list(dealers))} dealers")  # Debug print
        return JsonResponse({"dealers": list(dealers)})
    except Exception as e:
        print(f"Error in get_dealerships: {str(e)}")  # Debug print
        return JsonResponse({"error": str(e)}, status=500)

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request, dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...