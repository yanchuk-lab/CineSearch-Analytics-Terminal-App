"""
Utility module for handling interactive terminal menus and user input.
Provides functions for genre selection, year range input, and keyword search.
"""

from simple_term_menu import TerminalMenu
from formatter import print_films_paginated
from log_writer import create_log, insert_log
from mysql_connector import get_films_by_keyword

# Constants for terminal styling
RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"


def choose_genre(genres: list[str]) -> str | None:
    """
    Displays a genre selection menu with 'Back' and 'All Genres' options.
    """
    menu = TerminalMenu(
        ["Back"] + genres + ["All Genres"],
        title="\nSelect Genre:",
        menu_cursor="▶ ",
        menu_cursor_style=("fg_cyan", "bold"),
        cycle_cursor=True
    )
    choice_index = menu.show()

    if choice_index is None or choice_index == 0:
        return None
    elif choice_index == len(genres) + 1:
        return ""
    else:
        return genres[choice_index - 1]


def choose_year_range(min_year: int, max_year: int) -> tuple[str, str] | None:
    """
    Interactive menu for selecting a specific year or a range of years.
    Returns a tuple (low_limit_date, high_limit_date) or None to go back.
    """
    while True:
        menu = TerminalMenu(
            ["Back", "Enter Specific Year", f"Enter Year Range ({min_year}-{max_year})"],
            title="\nSelect Action:",
            menu_cursor="▶ ",
            menu_cursor_style=("fg_cyan", "bold")
        )
        choice = menu.show()

        if choice == 0 or choice is None:
            return None  # Back

        elif choice == 1:  # Specific Year
            year = input(f"Enter release year ({min_year}-{max_year}): ").strip()
            if not year.isdigit() or int(year) < min_year or int(year) > max_year:
                print(f"{RED}Year must be between {min_year} and {max_year}{RESET}")
                continue
            return year, year

        elif choice == 2:  # Year Range
            low_year = input(f"Enter min release year ({min_year}-{max_year}): ").strip()
            high_year = input("Enter max release year (Enter for same as min): ").strip()
            
            if not high_year:
                high_year = low_year

            if not low_year.isdigit() or not high_year.isdigit():
                print(f"{RED}Please enter numeric values!{RESET}")
                continue
                
            if (int(low_year) < min_year or int(low_year) > max_year or 
                    int(high_year) < min_year or int(high_year) > max_year):
                print(f"{RED}Years must be between {min_year} and {max_year}{RESET}")
                continue
                
            if int(high_year) < int(low_year):
                print(f"{RED}Max year cannot be less than min year!{RESET}")
                continue
                
            return low_year, high_year


def search_by_keyword() -> None:
    """
    Menu for keyword-based movie search.
    Handles user input, logging, and pagination display.
    """
    while True:
        menu = TerminalMenu(
            ["Enter Movie Title", "Back"],
            title="\nKeyword Search:",
            menu_cursor="▶ ",
            menu_cursor_style=("fg_cyan", "bold")
        )
        choice = menu.show()

        if choice == 0:  # Input keyword
            keyword = input("Enter movie title (Enter for all movies): ").strip()
            films = get_films_by_keyword(keyword)
            
            log_keyword = keyword if keyword else "'all_films'"
            insert_log(create_log("keyword", log_keyword, films))
            
            if not films:
                print(f"\n{YELLOW}No matches found. Please try again.{RESET}\n")
                continue
                
            print_films_paginated(films)
            return
            
        elif choice == 1 or choice is None:  # Back
            return