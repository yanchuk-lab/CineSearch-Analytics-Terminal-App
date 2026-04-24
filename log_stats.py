"""
Module for retrieving search statistics from MongoDB.
Includes functions for top frequent queries and recent search history.
"""

from pymongo import MongoClient
from config import config_mongo


def top_queries() -> list:
    """Returns a list of the top 5 most frequent search queries from MongoDB."""
    with MongoClient(**config_mongo) as client:
        db = client["ich_edit"]
        collection = db["final_project_230525-dam_sergii_yanchuk"]
        
        pipeline_top_queries = [
            {
                "$group": {
                    "_id": "$params.keyword",
                    "results_count": {"$sum": 1}
                }
            },
            {"$sort": {"results_count": -1}},
            {"$limit": 5},
        ]
        
        cursor = collection.aggregate(pipeline_top_queries)
        return list(cursor)


def last_queries() -> list:
    """Returns a list of the 5 most recent unique search queries from MongoDB."""
    with MongoClient(**config_mongo) as client:
        db = client["ich_edit"]
        collection = db["final_project_230525-dam_sergii_yanchuk"]
        
        pipeline_last_queries = [
            {"$sort": {"params.keyword": 1, "timestamp": -1}},
            {
                "$group": {
                    "_id": "$params.keyword",
                    "timestamp": {"$first": "$timestamp"},
                    "search_type": {"$first": "$search_type"},
                    "results_count": {"$first": "$results_count"},
                    "params": {"$first": "$params"},
                }
            },
            {"$sort": {"timestamp": -1}},
            {"$limit": 5},
        ]
        
        cursor = collection.aggregate(pipeline_last_queries)
        return list(cursor)