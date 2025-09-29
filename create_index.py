import redis
from redis.commands.search.field import TextField, TagField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

# Define the name of the index
INDEX_NAME = "movies_index"

def create_movie_index(r: redis.Redis):
    """
    Creates a RediSearch index for movies.
    
    Args:
        r: An active Redis connection object.
    """
    # Define the schema for the index
    # We map each field we want to search to a type (TEXT, TAG, NUMERIC, etc.)
    schema = (
        TextField("title", weight=5.0, sortable=True),
        TagField("genre", separator=','),
        NumericField("release_year", sortable=True)
        # Note: We are not indexing 'actors' or 'location' here because
        # they are stored as JSON strings, which are not ideal for direct indexing.
        # See the explanation below for the best way to handle them.
    )

    # Define the Index properties
    # We are targeting all HASH keys that start with the prefix "movie:"
    index_definition = IndexDefinition(prefix=["movie:"], index_type=IndexType.HASH)

    # Get the RediSearch client for the specific index
    rs = r.ft(INDEX_NAME)

    try:
        # Create the index with the defined schema and properties
        rs.create_index(schema, definition=index_definition)
        print(f"✅ Index '{INDEX_NAME}' created successfully.")
    except redis.exceptions.ResponseError as e:
        # This will happen if the index already exists
        if "Index already exists" in str(e):
            print(f"ℹ️ Index '{INDEX_NAME}' already exists. No action taken.")
        else:
            # Handle other potential errors
            print(f"🚨 An error occurred: {e}")


if __name__ == "__main__":
    try:
        # Connect to the Redis instance
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_client.ping()
        print("✅ Successfully connected to Redis.")

        # Run the index creation function
        create_movie_index(redis_client)

    except redis.exceptions.ConnectionError as e:
        print(f"🚨 Could not connect to Redis: {e}")
        print("Please ensure your Redis server is running with the RediSearch module.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("This may be because the RediSearch module is not loaded on your Redis server.")
        print("You can check by running 'MODULE LIST' in redis-cli.")
