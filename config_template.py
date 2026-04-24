"""
Configuration module for database connections.
This file contains credentials for MySQL and MongoDB.
"""

# MySQL Configuration (Sakila Database)
config_sql = {
    'host': 'YOUR_HOST_NAME',
    'user': 'YOUR_USER_NAME',
    'password': 'YOUR_PASSWORD',
    'database': 'sakila',
    'charset': 'utf8mb4'
}

# MongoDB Configuration (Logging System)
config_mongo = {
    'host': 'YOUR_MONGO_HOST',
    'username': 'YOUR_USERNAME',
    'password': 'YOUR_PASSWORD',
    'authMechanism': 'DEFAULT',
    'authSource': 'YOUR_AUTH_SOURCE',
    'readPreference': 'primary'
}