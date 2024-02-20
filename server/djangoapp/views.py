from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_request, get_dealers_from_cf, get_dealers_from_cf_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a different page after successful login
                return redirect('djangoapp:index')  # Change 'index' to the name of your home page URL pattern
            else:
                # Return an error message if authentication fails
                messages.error(request, 'Invalid username or password.')
        else:
            # Return form errors if form validation fails
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'djangoapp/login.html', {'form': form})

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    # Redirect to a different page after logout
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user object
            login(request, user)  # Log in the user
            # Redirect to a different page after successful registration
            return redirect('djangoapp:index')  # Change 'home' to the name of your home page URL pattern
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):

    if request.method == "GET":

        # Get dealers from the URL
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/57bfee28-6c6a-4668-87a7-1ade8a211a0f/Capstone/Get-all-dealerships"
        dealerships = get_dealers_from_cf(url)

        # Concat all dealer's short name
        context = {
            'id': [dealer.id for dealer in dealerships],
            'full_name': [dealer.full_name for dealer in dealerships],
            'address': [dealer.address for dealer in dealerships],
            'city': [dealer.city for dealer in dealerships],
            'st': [dealer.st for dealer in dealerships],
            'zip': [dealer.zip for dealer in dealerships],           
        }

        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealerships_by_ID` view to render a specific dealer at index
# def get_dealer_details(request, dealer_id):
# ...
def get_dealerships_by_ID(request, dealer_id):

    if request.method == "GET":

        # Get dealers from the URL
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/57bfee28-6c6a-4668-87a7-1ade8a211a0f/Capstone/Get-all-dealerships"
        dealerships = get_dealers_from_cf(url) #TODO: Change to function that retrieves dealer details by dealer_id

        # Concat all dealer's short name
        context = {
            'id': [dealer.id for dealer in dealerships],
            'full_name': [dealer.full_name for dealer in dealerships],
            'address': [dealer.address for dealer in dealerships],
            'city': [dealer.city for dealer in dealerships],
            'st': [dealer.st for dealer in dealerships],
            'zip': [dealer.zip for dealer in dealerships],           
        }

        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
    

# Create a "get_review" veiw to get all review

# Create a "get_review_by_Id" view to get a review at a specific id

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
