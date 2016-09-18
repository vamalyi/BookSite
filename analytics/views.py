from django.shortcuts import render

# Create your views here.
from django.conf import settings 
print(settings.DATABASES['default']['PASSWORD'])
