import pandas as pd
import requests  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

load_dotenv()

#env variable
API_KEY = os.getenv("API_KEY")

def get_url(movie_title: str):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(url)
    data = response.json()
    
    poster_path = data['results'][0].get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return None
    
def get_recommendations(movie_name: str):
    df = pd.read_csv("data/movie_dataset.csv")
    features = ['keywords', 'cast', 'genres', 'director']
    for feature in features:
        df[feature] = df[feature].fillna('')
    
    #create the sentence that will represent the movie with all the neceassy details from the movie  
    df["combined_features"] = df.apply(lambda row: row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director'], axis=1)
    
    movie_index = df[df['title'] == movie_name].index[0]

    cv = CountVectorizer()
    
    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    #contiains the titles, poster urls, and similarity scores of all the movies
    recommendations = []

    #skip over the first rec because it will be the exact same as the one entered
    #return only top 10 so it doesn't overwhelm the user
    for i in range(1, 11):
        title = df.iloc[sorted_similar_movies[i][0]]['title']
        poster_url = get_url(title)
        #add similarity score 
        similarity_score = round(sorted_similar_movies[i][1] * 100)
        recommendations.append({"title": title, "poster_url": poster_url, "similarity_score": similarity_score})
    
    return recommendations