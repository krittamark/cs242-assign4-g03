import urllib.request, urllib.parse, urllib.error
import json

serviceurl = "http://www.omdbapi.com/?"
apikey = "&apikey=4db1ee95"



def print_json(data):
    movie_data = ["Title", "Year", "Rated", "Released", "Runtime", "Genre", "Director","Writer", "Actors", "Plot", "Language", "Country", "Awards", "Poster",
                "Ratings", "Metascore", "imdbRating", "imdbVotes", "imdbID", "Type","DVD", "BoxOffice", "Production", "Website", "Response"]
    print("-" * 80)
    for key in movie_data:
        print(f"{key}: {data.get(key)}")
    print("-" * 80)

def search_movie(title):
    url = serviceurl + apikey + "&t=" + title
    try:
        response = urllib.request.urlopen(url)
        #print(response.getcode())
        data = json.loads(response.read().decode())
        #print(data)
        if data['Response'] == 'True':
            print_json(data)
        else:
            print(f"Error: {data.get('Error')}")
            return -1
        return 0
    except Exception as e:
        print(f"Error occurred: {e}")
        return -1

movie_name = input("Enter movie title: ")
search_movie(movie_name)

