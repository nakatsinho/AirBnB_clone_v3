#!/usr/bin/python3
"""Cities view module"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if 'name' not in data:
        abort(400, "Missing name")

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
