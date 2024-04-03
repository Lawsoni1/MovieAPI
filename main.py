"""Movie Watchlist program."""

try:
    import config
except ImportError:
    print(
        "Config file not found, create a new Python file called 'config.py' with the constant 'API_KEY' equal to your "
        "API key from omdbapi as a string")
    config = None
try:
    import requests
except ImportError:
    print(
        "The 'requests' library is not installed. Please install it using 'pip install requests' before running this "
        "program.")
    requests = None


class MovieAPI:
    """Class for interacting with OMDBAPI."""

    def __init__(self, base_url, search_url, title_url):
        """Initialize the MovieAPI class with base URLs."""
        self.base_url = base_url
        self.search_url = search_url
        self.title_url = title_url

    def make_request(self, url):
        """Make a request to the API."""
        response = requests.get(url)
        if response.status_code == 200:  # If somehow the URL is invalid or isn't working, this code prints out
            # whether the request was successful or not.
            json_data = response.json()
            return json_data
        else:
            print("API call failed.")
            return None

    def search_movies_by_title(self, title):
        """Create a URL to search for movies with the same name as 'title'."""
        url = self.base_url + self.search_url + f"={title}"  # Create URL
        search_data = self.make_request(url)  # Send URL to make request method which then returns the data.
        return search_data

    def get_movie_by_title(self, title):
        """Create a URL to get movie details by title."""
        url = self.base_url + self.title_url + f"={title}"  # Create URL
        title_data = self.make_request(url)  # Send URL to make request method which then returns the data.
        return title_data


class WatchList:
    """Class for managing a watch list of movies."""

    def __init__(self):
        """Initialize an empty watch list."""
        self.watch_list = []

    def show_all(self):
        """Show all movies in the watch list."""
        for index, movie in enumerate(self.watch_list, start=1):
            print(f"{index}. {movie}")

    def add_movie(self, title):
        """Add a movie to the watch list by appending it to the list watch_list."""
        if title in self.watch_list:
            print(f"\n{title} is already in your watchlist!")
        else:
            self.watch_list.append(title)
            print(
                f"\n{title} has been added to your watchlist!")  # This code checks whether the movie the user tries
            # to append already exists in the watchlist.

    def remove_movie(self, title):
        """Remove a movie from the watch list."""
        self.watch_list.remove(title)
        print(f"\n{title} has been removed from your watchlist!")


def search_movies(movie_api, watch_list):
    """Search for movies and manage watchlist."""
    title = input("\nEnter Movie Name: ")
    search_data = movie_api.search_movies_by_title(title)
    if 'Search' in search_data:  # Checks if the dictionary 'Search' is returned from API call, if it isn't, then an
        # error occurred and the program prints an error statement.
        count = 0
        movie_choices = []  # Empty list that stores all the returned data from API call, so it can be interacted
        # with later
        for movie in search_data['Search']:
            count += 1
            movie_choices.append(movie['Title'])
            print(f"{count}. {movie['Title']}")
        print(f"{len(movie_choices) + 1}. Exit")
        selected_movie = get_int(": ", "Invalid input, try again", 0, len(movie_choices) + 2)
        if selected_movie == len(movie_choices) + 1:
            print("")
            main()
        else:
            title_data = movie_api.get_movie_by_title(
                movie_choices[selected_movie - 1])  # Takes title name from movie and uses it in get_movie_by_title
            if title_data is not None:
                movie_data(title_data)
                print("\nDo You Wish to Add This Movie to Your Watchlist?")
                print("1. Yes")
                print("2. No")
                choice = get_int(": ", "Invalid input, try again", 0, 3)
                if choice == 1:
                    watch_list.add_movie(
                        movie_choices[selected_movie - 1])  # Appends selection by using add_movie method
    else:
        print("\nMovie not found!")


def movie_data(title_data):
    """Display movie details."""
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
    """View and manage the watch list."""
    while True:
        if watch_list.watch_list:
            print("\n|Watchlist|")
            watch_list.show_all()  # Calls WatchList function and show_all method
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
    """Main function to run the program."""
    movie_api = MovieAPI(f"http://www.omdbapi.com/?apikey={config.API_KEY}&", "s",
                         "t")  # Instance variable of MovieAPI class
    watch_list = WatchList()  # Instance variable of WatchList class
    while True:
        print("\n|Movie Watch List|")
        print("1. Search Movies By Title")
        print("2. View Watch List")
        print("3. Exit")
        choice = get_int(": ", "Invalid input, try again", 0, 4)
        if choice == 1:
            search_movies(movie_api, watch_list)
        elif choice == 2:
            view_watch_list(movie_api, watch_list)
        elif choice == 3:
            break


def get_int(msg, msg2, low, high):
    """Validation function to get an integer input within a range to validate all input from the user."""
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
