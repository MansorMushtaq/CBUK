import os
import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.http import JsonResponse
from datetime import datetime, date
from .forms import CovidDataForm
from django.contrib.auth import logout
import requests
from django.contrib import messages
from django.db import IntegrityError
import json
# Create your views here.

from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello from the COVID-19 app!")

@login_required
def dashboard(request):
    # Get the path to the CSV file in the same directory as this script
    csv_file_path = os.path.join(os.path.dirname(__file__), 'all-states-history.csv')

    # Initialize an empty list to store the CSV data
    csv_data = []

    # Initialize a set to keep track of unique state names
    unique_states = set()

    # Read the CSV file and populate the csv_data list
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            state = row['state']
            if state not in unique_states:
                csv_data.append(row)
                unique_states.add(state)
                
    username = request.session.get('username')
    # Define the API endpoint and parameters
    api_key = 'c64abb0ee6dd4c018da53519230709'
    location = 'pakistan'  # Replace with the desired location
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=7&aqi=no&alerts=no'

    # Make the API request
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract weather data for rendering
        dates = [forecast['date'] for forecast in data['forecast']['forecastday']]
        temperatures = [forecast['day']['avgtemp_c'] for forecast in data['forecast']['forecastday']]

        # Pass the data to the template
        context = {
            'dates': dates,
            'temperatures': temperatures,
        }

    # Pass the CSV data to the 'index.html' template
    return render(request, 'covid_19/dashboard/index.html', {'csv_data': csv_data , 'username': username, 'context': context})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # Attempt to save the form
                username = user.username
                request.session['username'] = username
                return redirect('covid_19:dashboard')
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                # Handle the IntegrityError or provide feedback to the user
    else:
        form = SignUpForm()

    return render(request, 'covid_19/registration/signup.html', {'form': form})
    # if request.method == 'POST':
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         return redirect('covid_19:dashboard')  # Redirect to the home page after successful signup
    # else:
    #     form = SignUpForm()
    # return render(request, 'covid_19/registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['username'] = user.username  # Store the username in session
            return redirect('covid_19:dashboard')  # Redirect to the dashboard page after successful login
    else:
        form = LoginForm()
    return render(request, 'covid_19/registration/login.html', {'form': form})

def new_record(request):
    if request.method == 'POST':
        form = CovidDataForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            cleaned_data = form.cleaned_data

            # Prepare the data as a dictionary with keys matching your CSV columns
            data_dict = {
    'date': cleaned_data['date'],
    'state': cleaned_data['state'],
    'death': cleaned_data['death'],
    'deathConfirmed': cleaned_data['deathConfirmed'],
    'deathIncrease': cleaned_data['deathIncrease'],
    'deathProbable': cleaned_data['deathProbable'],
    'hospitalized': cleaned_data['hospitalized'],
    'hospitalizedCumulative': cleaned_data['hospitalizedCumulative'],
    'hospitalizedCurrently': cleaned_data['hospitalizedCurrently'],
    'hospitalizedIncrease': cleaned_data['hospitalizedIncrease'],
    'inIcuCumulative': cleaned_data['inIcuCumulative'],
    'inIcuCurrently': cleaned_data['inIcuCurrently'],
    'negative': cleaned_data['negative'],
    'negativeIncrease': cleaned_data['negativeIncrease'],
    'negativeTestsAntibody': cleaned_data['negativeTestsAntibody'],
    'negativeTestsPeopleAntibody': cleaned_data['negativeTestsPeopleAntibody'],
    'negativeTestsViral': cleaned_data['negativeTestsViral'],
    'onVentilatorCumulative': cleaned_data['onVentilatorCumulative'],
    'onVentilatorCurrently': cleaned_data['onVentilatorCurrently'],
    'positive': cleaned_data['positive'],
    'positiveCasesViral': cleaned_data['positiveCasesViral'],
    'positiveIncrease': cleaned_data['positiveIncrease'],
    'positiveScore': cleaned_data['positiveScore'],
    'positiveTestsAntibody': cleaned_data['positiveTestsAntibody'],
    'positiveTestsAntigen': cleaned_data['positiveTestsAntigen'],
    'positiveTestsPeopleAntibody': cleaned_data['positiveTestsPeopleAntibody'],
    'positiveTestsPeopleAntigen': cleaned_data['positiveTestsPeopleAntigen'],
    'positiveTestsViral': cleaned_data['positiveTestsViral'],
    'recovered': cleaned_data['recovered'],
    'totalTestEncountersViral': cleaned_data['totalTestEncountersViral'],
    'totalTestEncountersViralIncrease': cleaned_data['totalTestEncountersViralIncrease'],
    'totalTestResults': cleaned_data['totalTestResults'],
    'totalTestResultsIncrease': cleaned_data['totalTestResultsIncrease'],
    'totalTestsAntibody': cleaned_data['totalTestsAntibody'],
    'totalTestsAntigen': cleaned_data['totalTestsAntigen'],
    'totalTestsPeopleAntibody': cleaned_data['totalTestsPeopleAntibody'],
    'totalTestsPeopleAntigen': cleaned_data['totalTestsPeopleAntigen'],
    'totalTestsPeopleViral': cleaned_data['totalTestsPeopleViral'],
    'totalTestsPeopleViralIncrease': cleaned_data['totalTestsPeopleViralIncrease'],
    'totalTestsViral': cleaned_data['totalTestsViral'],
    'totalTestsViralIncrease': cleaned_data['totalTestsViralIncrease'],
}


            # Define the file path to your CSV file
            csv_file_path = os.path.join(os.path.dirname(__file__), 'all-states-history.csv')

            # Write the data to the CSV file
            with open(csv_file_path, 'a', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=data_dict.keys())
                csv_writer.writerow(data_dict)

            # Redirect or display a success message
            return redirect('covid_19:dashboard')  # Replace 'success' with your actual success URL

    else:
        form = CovidDataForm()

    return render(request, 'covid_19/registration/newdate.html', {'form': form})

def get_death_data(request):
    state = request.GET.get('state', None)
    current_date = date.today().strftime("%Y-%m-%d")  # Get the current date in the same format as your CSV data
    csv_file_path = os.path.join(os.path.dirname(__file__), 'all-states-history.csv')

    # Initialize an empty list to store the CSV data
    csv_data = []

    # Read the CSV file and populate the csv_data list
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    # Find the matching row in your CSV data based on the 'state' and 'date' fields
    matching_rows = [row for row in csv_data if row['state'] == state and row['date'] == current_date]

    if matching_rows:
        # Calculate the sum of 'death', 'hospitalized', 'positive', and 'negative' for the matching rows
        total_death = sum(int(row['death']) for row in matching_rows)
        total_hospitalized = sum(int(row['hospitalized']) for row in matching_rows)
        total_positive = sum(int(row['positive']) for row in matching_rows)
        total_negative = sum(int(row['negative']) for row in matching_rows)

        return JsonResponse({
            'deaths': total_death,
            'hospitalized': total_hospitalized,
            'positive': total_positive,
            'negative': total_negative
        })
    else:
        return JsonResponse({
            'deaths': 0,
            'hospitalized': 0,
            'positive': 0,
            'negative': 0
        }) # Return a default value if the state or current date is not found

# def get_death_data(request):
#     state = request.GET.get('state', None)
#     static_date = '2021-03-07'  # Your desired static date
    
#     csv_file_path = os.path.join(os.path.dirname(__file__), 'all-states-history.csv')

#     # Initialize variables to store the totals
#     total_death = 0
#     total_hospitalized = 0
#     total_positive = 0
#     total_negative = 0

#     # Initialize a variable to count matching rows
#     matching_row_count = 0
#     csv_data = []
#     with open(csv_file_path, 'r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             csv_data.append(row)
#     # Read the CSV file and populate the csv_data list
#     # with open(csv_file_path, 'r') as csv_file:
#     #     csv_reader = csv.DictReader(csv_file)
        
#         for row in csv_data:
            
#             if row['state'] == state and row['date'] == static_date:
#                 try:
#                     # Try to convert the values to integers
#                     total_death += int(row['death'])
#                     total_hospitalized += int(row['hospitalized'])
#                     total_positive += int(row['positive'])
#                     total_negative += int(row['negative'])
#                     matching_row_count += 1
#                 except ValueError:
#                     # Handle the case where the values cannot be converted to integers
#                     pass

#     if matching_row_count > 0:
#         return JsonResponse({
#             'deaths': total_death,
#             'hospitalized': total_hospitalized,
#             'positive': total_positive,
#             'negative': total_negative
#         })
#     else:
#         return JsonResponse({
#             'deaths': 1,
#             'hospitalized': 1,
#             'positive': 0,
#             'negative': 0
#         })
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')  # Display a logout message
    return redirect('covid_19:login')

# def get_weather_data(location):
#     api_key = 'c64abb0ee6dd4c018da53519230709'  # Replace with your WeatherAPI API key
#     url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=7&aqi=no&alerts=no'

#     response = requests.get(url)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None