from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.db import models
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class CovidDataForm(forms.Form):
    date = forms.DateField()
    state = forms.CharField(max_length=255)
    death = forms.IntegerField()
    deathConfirmed = forms.IntegerField()
    deathIncrease = forms.IntegerField()
    deathProbable = forms.IntegerField()
    hospitalized = forms.IntegerField()
    hospitalizedCumulative = forms.IntegerField()
    hospitalizedCurrently = forms.IntegerField()
    hospitalizedIncrease = forms.IntegerField()
    inIcuCumulative = forms.IntegerField()
    inIcuCurrently = forms.IntegerField()
    negative = forms.IntegerField()
    negativeIncrease = forms.IntegerField()
    negativeTestsAntibody = forms.IntegerField()
    negativeTestsPeopleAntibody = forms.IntegerField()
    negativeTestsViral = forms.IntegerField()
    onVentilatorCumulative = forms.IntegerField()
    onVentilatorCurrently = forms.IntegerField()
    positive = forms.IntegerField()
    positiveCasesViral = forms.IntegerField()
    positiveIncrease = forms.IntegerField()
    positiveScore = forms.IntegerField()
    positiveTestsAntibody = forms.IntegerField()
    positiveTestsAntigen = forms.IntegerField()
    positiveTestsPeopleAntibody = forms.IntegerField()
    positiveTestsPeopleAntigen = forms.IntegerField()
    positiveTestsViral = forms.IntegerField()
    recovered = forms.IntegerField()
    totalTestEncountersViral = forms.IntegerField()
    totalTestEncountersViralIncrease = forms.IntegerField()
    totalTestResults = forms.IntegerField()
    totalTestResultsIncrease = forms.IntegerField()
    totalTestsAntibody = forms.IntegerField()
    totalTestsAntigen = forms.IntegerField()
    totalTestsPeopleAntibody = forms.IntegerField()
    totalTestsPeopleAntigen = forms.IntegerField()
    totalTestsPeopleViral = forms.IntegerField()
    totalTestsPeopleViralIncrease = forms.IntegerField()
    totalTestsViral = forms.IntegerField()
    totalTestsViralIncrease = forms.IntegerField()
    # Add fields for the rest of your columns here