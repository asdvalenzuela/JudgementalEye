import model
import csv

def load_users(session):
    # use u.user
    users_table = open("seed_data/u.user", "r")
    for line in users_table:
        aline = line.split("|")
        user_id, age, gender, occupation, zipcode = aline
        user = model.User()
        user.id = user_id
        user.age = age
        user.zipcode = zipcode
        session.add(user)
        session.commit()

def load_movies(session):
    # use u.item
    movies_table = open("seed_data/u.item", "r")
    for line in movies_table:
        aline = line.split("|")
        movie_id = aline[0]
        old_movie_title = aline[1]
        release_date = aline[2]
        imdb_url = aline[4]

        movie_title = ""
        
        for char in old_movie_title:
            while char != "(":
                movie_title = movie_title + char
            else:
                break

        movie = model.Movie()
        movie.id = movie_id
        movie.name = movie_title
        movie.released_at = release_date
        movie.imdb_url = imdb_url

        session.add(movie)
    
    session.commit()

def load_ratings(session):
    # use u.data
    ratings_table = open("seed_data/u.user", "r")
    for line in users_table:
        aline = line.split("|")
        user_id, age, gender, occupation, zipcode = aline
        user = model.User()
        user.id = user_id
        user.age = age
        user.zipcode = zipcode
        session.add(user)
        session.commit()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)

    session = model.connect()
    # load_users(session)
    load_movies(session)
