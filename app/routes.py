from flask import Blueprint, render_template, request, jsonify
from .recommendation import get_recommendations

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()  
    movie_name = data.get('movie_name')  
    recommendations = get_recommendations(movie_name)  
    return jsonify(recommendations=recommendations)  
