from flask import Blueprint, render_template, request
from .recommendation import get_recommendations

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/recommend')
def recommend():
    return render_template('test.html')
