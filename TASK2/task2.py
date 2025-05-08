import urllib.request, urllib.parse, urllib.error
import json
import os
import random

serviceurl = "http://www.omdbapi.com/?"
apikey = "&apikey=4db1ee95"

def print_json(data):
    movie_data = ["Title", "Year", "Rated", "Released", "Runtime", "Genre", "Director","Writer", "Actors", "Plot", "Language", "Country", "Awards", "Poster",
                "Ratings", "Metascore", "imdbRating", "imdbVotes", "imdbID", "Type","DVD", "BoxOffice", "Production", "Website", "Response"]
    print("-" * 80)
    for key in movie_data:
        print(f"{key}: {data.get(key)}")
    print("-" * 80)

def save_poster(data):
    poster_url = data.get("Poster")
    #print(f"Poster URL: {poster_url}")
    title = data.get("Title")
    title.replace(" ", "_")
    if poster_url not in (None, "", "N/A"):
        try:
            filename = f"{title}_poster_6609612152.jpg"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(script_dir, filename)
            response = urllib.request.urlopen(poster_url)
            image = response.read()
            response.close()
            f = open(filepath, "wb")
            f.write(image)
            f.close()
        except Exception as e:
            print(f"Error saving poster: {e}")
    else:
        print("Poster not available.")

def search_movie(title):
    title = urllib.parse.quote(title)
    url = serviceurl + apikey + "&t=" + title
    try:
        response = urllib.request.urlopen(url)
        #print(response.getcode())
        data = json.loads(response.read().decode())
        #print(data)
        response.close()
        if data['Response'] == 'True':
            print_json(data)
            save_poster(data)
        else:
            print(f"Error: {data.get('Error')}")
            return -1
        return 0
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
        return -1
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}")
        return -1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return -1


movie_name = input("Enter movie title: ")
search_movie(movie_name)

