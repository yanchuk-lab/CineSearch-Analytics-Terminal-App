"""
Module for formatting and displaying movie data in the terminal.
Maintains original logic and naming conventions while following PEP 8.
"""

from simple_term_menu import TerminalMenu
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED

# Color constants for terminal output
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

console = Console()


def print_films_paginated(films: tuple[tuple]) -> None:
    """
    Prints films page by page. 
    Fixed to handle NULL/None values from the database safely.
    """
    if not films:
        print(f"{YELLOW}No matches found{RESET}")
        return

    # Use str(film[x] or "") to ensure we never call len() on a None object
    max_title_len = max(len(str(film[1] or "")) for film in films) + 2
    max_year_len = max(len(str(film[2] or "")) for film in films) + 2
    max_genre_len = max(len(str(film[3] or "")) for film in films) + 2
    
    print()
    print(f"{GREEN}Total films found: {len(films)}{RESET}")

    page_size = 10
    for start in range(0, len(films), page_size):
        table = Table(box=ROUNDED)
        table.add_column("Title", width=max_title_len)
        table.add_column("Year", width=max_year_len, justify="center")
        table.add_column("Genre", width=max_genre_len)

        for film in films[start:start + page_size]:
            # Replace None with "N/A" for a clean terminal look
            display_title = str(film[1]) if film[1] is not None else "Unknown"
            display_year = str(film[2]) if film[2] is not None else "N/A"
            display_genre = str(film[3]) if film[3] is not None else "N/A"
            
            table.add_row(display_title, display_year, display_genre)

        console.print(table)

        if start + page_size < len(films):
            menu = TerminalMenu(
                ["Show More", "Exit"],
                title="\nSelect an action:",
                menu_cursor="▶ ",
                menu_cursor_style=("fg_cyan", "bold")
            )
            choice = menu.show()
            if choice == 1:
                return


def get_top(top_queries: list) -> None:
    """Displays TOP-5 most frequent search queries."""
    if not top_queries:
        print("No data available")
        return

    table = Table(title="TOP-5 Queries", box=ROUNDED)
    table.add_column("№", justify="center")
    table.add_column("Query")
    table.add_column("Count", justify="center")

    for i, doc in enumerate(top_queries, start=1):
        table.add_row(str(i), str(doc['_id']), str(doc['results_count']))

    console.print(table)


def get_last(last_queries: list) -> None:
    """Displays the last 5 unique search queries."""
    if not last_queries:
        print("No data available")
        return

    table = Table(title="Last 5 Queries", box=ROUNDED)
    table.add_column("№", justify="center")
    table.add_column("Query")
    table.add_column("Results", justify="center")

    for i, doc in enumerate(last_queries, start=1):
        table.add_row(str(i), str(doc['params']['keyword']), str(doc['results_count']))

    console.print(table)
