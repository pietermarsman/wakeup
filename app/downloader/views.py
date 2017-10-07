from django.shortcuts import render
from django.views.generic import ListView

from downloader.models import Top40Song


class Top40List(ListView):
    model = Top40Song
