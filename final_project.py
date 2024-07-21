
import json
import requests_with_caching

def get_movies_from_tastedive(input):
    parameters = {"q": input, "type": "movies", "limit": 5}
    tastedive_response = requests_with_caching.get("https://tastedive.com/api/similar", params=parameters)
    data = json.loads(tastedive_response.text)
    return data

def extract_movie_titles(result):
    my_list = []
    dictionary = result['Similar']['Results']
    for r in dictionary:
        print(r['Name'])
        my_list.append(r['Name'])
    return my_list

def get_related_titles(a_list):
    master_list = []
    seen = set(master_list)
    for i in a_list:
        data = get_movies_from_tastedive(i)
        another_list = extract_movie_titles(data)
        for j in another_list:
            if j not in seen:
                master_list.append(j)
            seen = set(master_list)
    return master_list

def get_movie_data(input):
    parameters = {"t": input, "r": "json"}
    tastedive_response = requests_with_caching.get("http://www.omdbapi.com/", params=parameters)
    data = json.loads(tastedive_response.text)
    return data

def get_movie_rating(handle):
    b_list = (handle['Ratings'])
    for i in b_list:
        if i['Source'] == 'Rotten Tomatoes':
            percentage = i['Value']
            percentage_int = int(percentage.strip('%'))
            print(percentage_int)
            return percentage_int

# Define the get_sorted_recommendations function
def get_sorted_recommendations(movie_titles):
    related_titles = get_related_titles(movie_titles)
    ratings = list()
    sorted_list = list()
    for movie in related_titles:
        a = get_movie_data(movie)
        ratings.append(get_movie_rating(a))

    sorted_list = sorted(ratings, reverse=True)
    return ratings


get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])