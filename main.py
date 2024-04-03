import config
try:
    import requests
except ImportError:
    print("The 'requests' library is not installed. Please install it using 'pip install requests' before running this program.")


class MovieAPI:
    def __init__(self, base_url, search_url, title_url):
        self.base_url = base_url
        self.search_url = search_url
        self.title_url = title_url

    def make_request(self, url):
        print("Making request...")
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


class WatchList:
    def __init__(self):
        self.watch_list = []

    def show_all(self):
        print("")
        for index, movie in enumerate(self.watch_list, start=1):
            print(f"{index}. {movie}")

    def add_movie(self, title):
        if 'title' in self.watch_list:
            print(f"\n{title} is already in your watchlist!")
        else:
            self.watch_list.append(title)
            print(f"\n{title} has been added to your watchlist!")

    def remove_movie(self, title):
        self.watch_list.remove(title)
        print(f"\n{title} has been removed from your watchlist!")


def search_movies(movie_api, watch_list):
    print("\nEnter Movie Name")
    title = input(": ")
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
        print(f"{len(movie_choices) + 1}. Exit")
        print("\nSelect Movie by Number or Exit")
        selected_movie = get_int(": ", "Invalid input, try again", 0, len(movie_choices) + 2)
        print("")
        if selected_movie == len(movie_choices) + 1:
            print("")
            main()
        else:
            title_data = movie_api.get_movie_by_title(movie_choices[selected_movie - 1])
            if title_data is not None:
                movie_data(title_data)
                print("\nDo You Wish to Add This Movie to Your Watchlist?")
                print("1. Yes")
                print("2. No")
                choice = get_int(": ", "Invalid input, try again", 0, 3)
                if choice == 1:
                    watch_list.add_movie(movie_choices[selected_movie - 1])
    else:
        print("\nMovie not found!")


def movie_data(title_data):
    print("\n|Movie Data|")
    if title_data is not None:
        print(f"\nTitle: {title_data['Title']}")
        print(f"Year: {title_data['Year']}")
        print(f"Rated: {title_data['Rated']}")
        print(f"Released: {title_data['Released']}")
        print(f"Runtime: {title_data['Runtime']}")
        print(f"Genre: {title_data['Genre']}")
        print(f"Director(s): {title_data['Director']}")
        print(f"Writer(s): {title_data['Writer']}")
        print(f"Actors: {title_data['Actors']}")
        print(f"Plot: {title_data['Plot']}")
        print(f"Language: {title_data['Language']}")
        print(f"Country: {title_data['Country']}")
        print(f"Awards: {title_data['Awards']}")
        return title_data


def view_watch_list(movie_api, watch_list):
    while True:
        if watch_list.watch_list:
            print("\n|Watchlist|")
            watch_list.show_all()
            print("\nDo you wish to add or remove a movie?")
            print("1. Add")
            print("2. Remove")
            print("3. View Movie")
            print("4. Exit")
            choice = get_int(": ", "Invalid input, try again", 0, 5)
            if choice == 1:
                search_movies(movie_api, watch_list)
            elif choice == 2:
                print("\nSelect Movie by Number")
                choice = get_int(": ", "Invalid input, try again", 0, len(watch_list.watch_list) + 1)
                watch_list.remove_movie(watch_list.watch_list[choice - 1])
            elif choice == 3:
                print("\nSelect Movie by Number")
                selected_movie = get_int(": ", "Invalid input, try again", 0, 3)
                title_data = movie_api.get_movie_by_title(watch_list.watch_list[selected_movie - 1])
                movie_data(title_data)
            elif choice == 4:
                break
        else:
            print("\nYour watchlist is empty!")
            break

def main():
    movie_api = MovieAPI(f"http://www.omdbapi.com/?apikey={config.API_KEY}&", "s", "t")
    watch_list = WatchList()
    while True:
        print("\n|Movie Watch List|")
        print("\n1. Search Movies By Title")
        print("2. View Watch List")
        print("3. Exit ")
        choice = get_int(": ", "Invalid input, try again", 0, 4)
        if choice == 1:
            search_movies(movie_api, watch_list)
        elif choice == 2:
            view_watch_list(movie_api, watch_list)
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
