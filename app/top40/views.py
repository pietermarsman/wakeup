from django.shortcuts import render
from django.views.generic import ListView

from top40.models import Top40Song


class Top40List(ListView):
    model = Top40Song
