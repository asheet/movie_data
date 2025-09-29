#!/usr/bin/env python3
"""
MongoDB Error Codes Insertion Script

This script connects to a MongoDB database and inserts sample error codes
with their descriptions into a collection.
"""

import pymongo
from pymongo import MongoClient
import sys

def create_sample_error_data():
    """Create sample error code data with descriptions"""
    error_codes = [
        {
            "error_code": "E001",
            "description": "Invalid user credentials provided",
            "category": "Authentication",
            "severity": "High"
        },
        {
            "error_code": "E002", 
            "description": "Database connection timeout",
            "category": "Database",
            "severity": "Critical"
        },
        {
            "error_code": "E003",
            "description": "Insufficient permissions to access resource",
            "category": "Authorization",
            "severity": "Medium"
        },
        {
            "error_code": "E004",
            "description": "Invalid request format - missing required fields",
            "category": "Validation",
            "severity": "Medium"
        },
        {
            "error_code": "E005",
            "description": "Service temporarily unavailable",
            "category": "Service",
            "severity": "High"
        },
        {
            "error_code": "E006",
            "description": "File not found or access denied",
            "category": "File System",
            "severity": "Medium"
        },
        {
            "error_code": "E007",
            "description": "Network connection lost",
            "category": "Network",
            "severity": "High"
        },
        {
            "error_code": "E008",
            "description": "Memory allocation failed",
            "category": "System",
            "severity": "Critical"
        },
        {
            "error_code": "E009",
            "description": "Invalid configuration parameters",
            "category": "Configuration",
            "severity": "Medium"
        },
        {
            "error_code": "E010",
            "description": "Rate limit exceeded",
            "category": "Throttling",
            "severity": "Low"
        }
    ]
    return error_codes

def connect_to_mongodb(connection_string="mongodb://localhost:27017/"):
    """
    Connect to MongoDB database
    
    Args:
        connection_string (str): MongoDB connection string
        
    Returns:
        MongoClient: MongoDB client instance
    """
    try:
        client = MongoClient(connection_string)
        # Test the connection
        client.admin.command('ping')
        print(f"Successfully connected to MongoDB at {connection_string}")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while connecting: {e}")
        sys.exit(1)

def insert_error_codes(client, database_name="error_tracking", collection_name="error_codes"):
    """
    Insert error codes into MongoDB collection
    
    Args:
        client (MongoClient): MongoDB client instance
        database_name (str): Name of the database
        collection_name (str): Name of the collection
    """
    try:
        # Access database and collection
        db = client[database_name]
        collection = db[collection_name]
        
        # Get sample data
        error_data = create_sample_error_data()
        
        # Insert the data
        result = collection.insert_many(error_data)
        
        print(f"Successfully inserted {len(result.inserted_ids)} error codes into '{database_name}.{collection_name}'")
        print(f"Inserted document IDs: {result.inserted_ids}")
        
        # Display inserted data
        print("\nInserted Error Codes:")
        print("-" * 80)
        for doc in collection.find():
            print(f"Code: {doc['error_code']}")
            print(f"Description: {doc['description']}")
            print(f"Category: {doc['category']}")
            print(f"Severity: {doc['severity']}")
            print("-" * 80)
            
    except pymongo.errors.DuplicateKeyError as e:
        print(f"Duplicate key error: {e}")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

def main():
    """Main function to execute the script"""
    print("MongoDB Error Codes Insertion Script")
    print("=" * 50)
    
    # Configuration
    connection_string = "mongodb://localhost:27017/"
    database_name = "error_tracking"
    collection_name = "error_codes"
    
    # You can modify these values or make them command line arguments
    if len(sys.argv) > 1:
        connection_string = sys.argv[1]
    if len(sys.argv) > 2:
        database_name = sys.argv[2]
    if len(sys.argv) > 3:
        collection_name = sys.argv[3]
    
    print(f"Connection String: {connection_string}")
    print(f"Database: {database_name}")
    print(f"Collection: {collection_name}")
    print()
    
    # Connect to MongoDB
    client = connect_to_mongodb(connection_string)
    
    try:
        # Insert error codes
        insert_error_codes(client, database_name, collection_name)
        
    finally:
        # Close the connection
        client.close()
        print("\nMongoDB connection closed.")

if __name__ == "__main__":
    main()
