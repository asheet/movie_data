import redis

def populate_movie_data(r: redis.Redis):
    """
    Populates a Redis database with sample data about movies, actors, and theaters.

    Args:
        r: An active Redis connection object.
    """
    print("Connecting to Redis and clearing existing data...")
    # Clear the database to ensure a fresh start for this script
    r.flushdb()

    # --- Sample Data ---
    movies = {
        'movie:1': {'title': 'The Grand Heist', 'genre': 'Sci-Fi', 'release_year': '2025'},
        'movie:2': {'title': 'Echoes of the Void', 'genre': 'Thriller', 'release_year': '2024'},
        'movie:3': {'title': 'Sunset Boulevard 2.0', 'genre': 'Drama', 'release_year': '2025'}
    }
    
    # NEW movies
    more_movies = {
        'movie:4': {'title': 'Cosmic Chuckles', 'genre': 'Comedy', 'release_year': '2024'},
        'movie:5': {'title': 'Velocity Edge', 'genre': 'Action', 'release_year': '2025'},
        'movie:6': {'title': 'The Silicon Age', 'genre': 'Documentary', 'release_year': '2023'},
        'movie:7': {'title': 'Parisian Promise', 'genre': 'Romance', 'release_year': '2025'}
    }
    movies.update(more_movies)

    actors = {
        'actor:1': {'name': 'Leo Vance'},
        'actor:2': {'name': 'Kara Nova'},
        'actor:3': {'name': 'Sam "The Rock" Johnson'},
        'actor:4': {'name': 'Elara Finch'}
    }

    # NEW actors
    more_actors = {
        'actor:5': {'name': 'Miles O\'Brien'},
        'actor:6': {'name': 'Jian Li'},
        'actor:7': {'name': 'Sofia Rossi'},
        'actor:8': {'name': 'Markus Thorne'}
    }
    actors.update(more_actors)
    
    theaters = {
        'theater:1': {'name': 'Frisco Cineplex', 'location': 'Frisco, TX'},
        'theater:2': {'name': 'Downtown Movie Palace', 'location': 'Dallas, TX'}
    }
    
    # NEW theater
    more_theaters = {
        'theater:3': {'name': 'Plano Premiere Cinema', 'location': 'Plano, TX'}
    }
    theaters.update(more_theaters)

    # --- Relationships ---
    movie_actors = {
        'movie:1': ['actor:1', 'actor:2'],
        'movie:2': ['actor:2', 'actor:4'],
        'movie:3': ['actor:3', 'actor:1', 'actor:4']
    }
    
    # NEW relationships
    more_movie_actors = {
        'movie:4': ['actor:5', 'actor:7'],
        'movie:5': ['actor:3', 'actor:8'],
        'movie:6': ['actor:4'], # Narrator
        'movie:7': ['actor:6', 'actor:7']
    }
    movie_actors.update(more_movie_actors)

    theater_movies = {
        'theater:1': ['movie:1', 'movie:3'],
        'theater:2': ['movie:2', 'movie:3']
    }
    
    # NEW relationships
    more_theater_movies = {
        'theater:1': ['movie:5'], # Frisco also playing the new action movie
        'theater:2': ['movie:4'], # Dallas also playing the new comedy
        'theater:3': ['movie:1', 'movie:6', 'movie:7'] # Plano showing a mix
    }
    # Special handling for extending sets
    for theater, movies_to_add in more_theater_movies.items():
        if theater in theater_movies:
            theater_movies[theater].extend(movies_to_add)
        else:
            theater_movies[theater] = movies_to_add
    

    # --- Inserting Data into Redis ---

    # 1. Add Movies, Actors, and Theaters as Hashes
    # HASH is great for storing object-like data.
    print("Adding movies, actors, and theaters...")
    for collection in [movies, actors, theaters]:
        for key, data in collection.items():
            r.hset(key, mapping=data)

    # 2. Add Relationships using Sets
    # SETS are ideal for relationships because they are unordered and store unique members.
    print("Building relationships...")
    
    # Link actors to movies
    for movie_id, actor_ids in movie_actors.items():
        # The key is descriptive, e.g., 'movie:1:actors'
        r.sadd(f'{movie_id}:actors', *actor_ids)

    # Link movies to theaters
    for theater_id, movie_ids in theater_movies.items():
        # The key is descriptive, e.g., 'theater:1:movies'
        r.sadd(f'{theater_id}:movies', *movie_ids)
        
    print("\n✅ Data insertion complete!")

def verify_data(r: redis.Redis):
    """
    Fetches and prints some sample data to verify it was inserted correctly.
    
    Args:
        r: An active Redis connection object.
    """
    print("\n--- Verifying Data ---")

    # Get details for 'The Grand Heist' (movie:1)
    movie_1_details = r.hgetall('movie:1')
    print(f"Details for movie:1 -> {movie_1_details}")

    # Get the set of actors for 'The Grand Heist'
    movie_1_actor_ids = r.smembers('movie:1:actors')
    print(f"Actor IDs for movie:1 -> {movie_1_actor_ids}")

    # --- VERIFYING NEW DATA ---
    print("\n--- Verifying NEW Data ---")

    # Get details for 'Velocity Edge' (movie:5)
    movie_5_details = r.hgetall('movie:5')
    print(f"Details for new movie 'Velocity Edge' (movie:5) -> {movie_5_details}")

    # Get the actors for 'Velocity Edge', including one old and one new actor
    movie_5_actor_ids = r.smembers('movie:5:actors')
    actor_names = [r.hget(actor_id, 'name') for actor_id in movie_5_actor_ids]
    print(f"Actor names for movie:5 -> {actor_names}")

    # Get the movies playing at the new 'Plano Premiere Cinema' (theater:3)
    plano_theater_name = r.hget('theater:3', 'name')
    plano_movie_ids = r.smembers('theater:3:movies')
    movie_titles = [r.hget(movie_id, 'title') for movie_id in plano_movie_ids]
    print(f"\nMovies playing at '{plano_theater_name}': {movie_titles}")


if __name__ == "__main__":
    try:
        # Connect to a local Redis instance
        # The `decode_responses=True` argument ensures that Redis returns strings, not bytes.
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # Check if the server is available
        redis_client.ping()
        
        # Run the functions
        populate_movie_data(redis_client)
        verify_data(redis_client)

    except redis.exceptions.ConnectionError as e:
        print(f"🚨 Could not connect to Redis: {e}")
        print("Please ensure your Redis server is running.")
