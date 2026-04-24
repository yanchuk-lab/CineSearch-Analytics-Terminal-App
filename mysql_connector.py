"""
Module for handling MySQL database interactions.
Contains SQL queries and functions to fetch movie data, genres, and date ranges.
"""

import pymysql
from config import config_sql

# SQL Queries for better readability (Standard Industry Practice)
QUERY_BY_KEYWORD = """
    SELECT film.film_id, film.title, film.release_year, category.name
    FROM film
    LEFT JOIN film_category ON film.film_id = film_category.film_id
    LEFT JOIN category ON film_category.category_id = category.category_id
    WHERE title LIKE %s
"""

QUERY_BY_GENRE = """
    SELECT film.film_id, film.title, film.release_year, category.name
    FROM film
    LEFT JOIN film_category ON film.film_id = film_category.film_id
    LEFT JOIN category ON film_category.category_id = category.category_id
    WHERE (release_year BETWEEN %s AND %s OR release_year = %s) 
    AND name LIKE %s
"""

QUERY_ALL_GENRES = "SELECT DISTINCT name FROM category"

QUERY_YEAR_RANGE = "SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year FROM film"


def get_films_by_keyword(keyword: str) -> tuple:
    """Returns movies that contain the specified keyword in their title."""
    with pymysql.connect(**config_sql) as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_BY_KEYWORD, (f'%{keyword}%',))
            return cursor.fetchall()


def get_genres() -> list[str]:
    """Returns a list of all available movie genres from the database."""
    with pymysql.connect(**config_sql) as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_ALL_GENRES)
            return [genre[0] for genre in cursor.fetchall()]


def get_date_range() -> tuple[int, int]:
    """Returns the minimum and maximum release years found in the database."""
    with pymysql.connect(**config_sql) as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_YEAR_RANGE)
            result = cursor.fetchone()
            return result[0], result[1]


def get_films_by_genre_and_date(low_limit_date: str, genre: str = "", high_limit_date: str = "") -> tuple[tuple]:
    """Returns movies filtered by genre and a specific year range."""
    with pymysql.connect(**config_sql) as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_BY_GENRE, (low_limit_date, high_limit_date, low_limit_date, f"%{genre}%"))
            return cursor.fetchall()


