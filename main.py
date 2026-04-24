"""
Main entry point for the Cinema Search Engine application.
Handles the primary menu loop and coordinates between MySQL and MongoDB modules.
"""

import pymysql
import pymongo
from pymongo.errors import OperationFailure
from simple_term_menu import TerminalMenu
from rich.console import Console

from mysql_connector import (
    get_genres,
    get_date_range,
    get_films_by_genre_and_date
)
from log_writer import create_log, insert_log
from log_stats import top_queries, last_queries
from formatter import print_films_paginated, get_top, get_last
from menu_utils import choose_genre, choose_year_range, search_by_keyword

# Constants for terminal styling
RESET = "\033[0m"
RED = "\033[31m"
CYAN = "\033[36m"

console = Console()


def main():
    """
    Executes the main application loop.
    Provides an interactive menu for movie searching and analytics.
    """
    while True:
        try:
            options = [
                "Search by Keyword",
                "Search by Genre and Year",
                "TOP-5 Frequent Queries",
                "Last 5 Unique Searches",
                "Exit"
            ]
            terminal_menu = TerminalMenu(
                options,
                title="\n  ========= MAIN MENU =========",
                menu_cursor="▶ ",
                menu_cursor_style=("fg_cyan", "bold")
            )
            selection_index = terminal_menu.show()

            if selection_index == 0:
                search_by_keyword()

            elif selection_index == 1:
                genre = choose_genre(get_genres())
                if genre is None:
                    continue

                min_year, max_year = get_date_range()
                year_range = choose_year_range(min_year, max_year)
                if year_range is None:
                    continue
                low_limit_date, high_limit_date = year_range

                films = get_films_by_genre_and_date(
                    low_limit_date, genre, high_limit_date
                )
                
                # Logic for creating a descriptive keyword for the log
                composite_keyword = (f"{genre}_{low_limit_date}").strip("_")
                if high_limit_date != low_limit_date:
                    composite_keyword += f"_{high_limit_date}"
                
                # Logging to MongoDB and displaying results
                insert_log(create_log("genre_date", composite_keyword, films))
                print_films_paginated(films)

            elif selection_index == 2:
                get_top(top_queries())

            elif selection_index == 3:
                get_last(last_queries())

            elif selection_index == 4 or selection_index is None:
                print(f"{CYAN}Exiting program...{RESET}")
                break

        except (pymysql.MySQLError, ConnectionError, TimeoutError):
            print(f"{RED}MySQL Error: A database connection error occurred.{RESET}")
        except (pymongo.errors.PyMongoError, ConnectionError, TimeoutError):
            print(f"{RED}MongoDB Error: A database connection error occurred.{RESET}")
        except OperationFailure:
            print(f"{RED}Auth Error: Check your MongoDB credentials.{RESET}")


if __name__ == "__main__":
    main()