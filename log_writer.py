"""
Module for writing search logs to MongoDB.
Handles log creation and database insertion.
"""

from datetime import datetime
from pymongo import MongoClient
from config import config_mongo


def create_log(search_type: str, keyword: str, films: tuple[tuple]) -> dict:
    """
    Creates a log dictionary with search query details.
    
    Args:
        search_type: The category of search (keyword or genre_date).
        keyword: The search term used.
        films: The results obtained to calculate the count.
    """
    now = datetime.now()
    return {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "search_type": search_type,
        "params": {"keyword": keyword},
        "results_count": len(films)
    }


def insert_log(log: dict) -> None:
    """Inserts the generated log dictionary into the MongoDB collection."""
    with MongoClient(**config_mongo) as client:
        db = client["ich_edit"]
        collection = db["final_project_230525-dam_sergii_yanchuk"]
        collection.insert_one(log)