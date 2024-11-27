from django.shortcuts import render
from django.views.generic import TemplateView
from applications.caja.models import Caja

# Create your views here.


class Home(TemplateView):
    template_name = "home/index.html"



