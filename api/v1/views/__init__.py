#!/usr/bin/python3
"""
Contains the blueprint for the API
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views here
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import  # Add this line to import the cities view

