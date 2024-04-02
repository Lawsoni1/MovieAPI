from typing import Any
import requests

class MovieAPI:
    def __init__(self, base_url, search_url, title_url):
        self.base_url = base_url
        self.search_url = search_url
        self.title_url = title_url

    def make_request(self, url):
        print("Making Request...")
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print("API call failed.")
            return None

    def search_movies_by_title(self, title):
        print(f"Finding movie(s) with the name {title}...")
        url = self.base_url + self.search_url + f"={title}"
        search_data = self.make_request(url)
        return search_data
    
    def get_movie_by_title(self, title):
        print(f"Finding information about {title}...")
        url = self.base_url + self.title_url + f"={title}"
        search_data = self.make_request(url)
        return search_data


def main():
    movie_api = MovieAPI("http://www.omdbapi.com/?apikey=15f4926e&", "s", "t")
    print("Movie Watch List")
    while True:
        print("\n1. Search Movies By Title")
        print("2. Exit ")
        choice = get_int(": ", "Invalid Input, Try Again", 0, 3)
        print("")
        if choice == 1:
            print("Enter Movie Name")
            title = input("\n: ")
            print("")
            search_data = movie_api.search_movies_by_title(title)
            if 'Search' in search_data:
                print("")
                count = 0
                movie_choices = []
                for movie in search_data['Search']:
                    count += 1
                    movie_choices.append(movie['Title'])
                    print(f"{count}. {movie['Title']}")
                print("\nSelect a movie by number: ")
                selected_movie = get_int(": ", "Invalid Input, Try Again", 0, len(movie_choices) + 1)
                title_data = movie_api.get_movie_by_title(movie_choices[selected_movie - 1])
                if title_data is not None:
                    print(f"\nTitle: {title_data['Title']}")
                    print(f"Plot: {title_data['Plot']}")
            else:
                print("\nMovie not found!")

        elif choice == 2:
            break

def get_int(msg, msg2, low, high):
    while True:
        try:
            num = int(input(msg))
            if low < num < high:
                return num
            else:
                print(msg2)
        except ValueError:
            print(msg2)

if __name__ == '__main__':
    main()
