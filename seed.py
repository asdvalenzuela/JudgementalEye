import model
import csv
import datetime

def load_users(session):
    # use u.user
    #reads in file and parses data
    users_table = open("seed_data/u.user", "r")
    for line in users_table:
        aline = line.split("|")
        user_id, age, gender, occupation, zipcode = aline
        
        #creates instance of user
        user = model.User()
        user.id = user_id
        user.age = age
        user.zipcode = zipcode

        #adds user to session
        session.add(user)
    
    #commits session changes
    session.commit()

def load_movies(session):
    # use u.item
    #reads in file and parses data
    movies_table = open("seed_data/u.item", "r")
    for line in movies_table:
        aline = line.split("|")
        movie_id = aline[0]
        old_movie_title = aline[1]
        release_date = aline[2]
        imdb_url = aline[4]
        
        #removes date from movie title column
        movie_title = old_movie_title.split("(")
        new_movie_title = movie_title[0]
        #converts to unicode
        new_movie_title = new_movie_title.decode("latin-1")

        #parses date to pass to datetime function
        release_date = release_date.split("-")
        day, month, year = release_date
        months = {"Jan":1,"Feb":2, "Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7, "Aug":8, "Sep":9, "Oct":10,"Nov":11,"Dec":12}
        date = datetime.date(int(year), months[month], int(day))

        #creates instance of movie
        movie = model.Movie()
        movie.id = movie_id
        movie.name = new_movie_title
        movie.released_at = date
        movie.imdb_url = imdb_url

        #adds movie to session
        session.add(movie)

    #commits session changes
    session.commit()

def load_ratings(session):
    # use u.data
        #user id | item id | rating | timestamp. 

    ratings_table = open("seed_data/u.data", "r")
    for line in ratings_table:
        aline = line.split()
        user_id, item_id, rating, timestamp = aline
        rating = model.Rating()
        
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
