import requests

class MovieAPI:
    def __init__(self, base_url, search_url):
        self.base_url = base_url
        self.search_url = search_url

    def make_request(self, url):
        # Makes request to quote website and returns the data
        print("Making Request...")
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print("API call failed.")
            return None

    def get_movie_by_title(self, title):
        print(f"Finding movie(s) with the name {title}...")
        url = self.base_url + self.search_url + f"={title}"
        search_data = self.make_request(url)
        return search_data

def main():
    movie_api = MovieAPI("http://www.omdbapi.com/?apikey=15f4926e&", "s")
    print("Movie Watch List")
    while True:
        print("\nSearch Movies By Title (1)")
        choice = get_int(": ", "Invalid Input, Try Again", 0, 3)
        if choice == 1:
            print("Enter movie name")
            title = input("\n: ")
            search_data = movie_api.get_movie_by_title(title)
            if search_data is not None and 'Search' in search_data:
                for movie in search_data['Search']:
                    print(movie['Title'])
        elif choice == 2:
            pass
        elif choice == 3:
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
