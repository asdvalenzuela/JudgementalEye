from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE = create_engine("sqlite:///ratings.db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE,
                                        autocommit = False,
                                        autoflush = False))

# ENGINE = None
# Session = None


Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)

    # creates backref relationship to Rating class
    ratings = relationship("Rating")

#defines movie class
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable = False)
    released_at = Column(Date(timezone=False), nullable = True)
    imdb_url = Column(String(300), nullable=True)

    # ratings backref added by Rating class

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    rating = Column(Integer, nullable = True)
    #connects to User class, can order by name, timestamp, etc.
    #with this one we added the relationship in the User class, this can be done either way
    user = relationship("User")

    #connects to Movie class
    movie = relationship("Movie", 
        backref=backref("ratings", order_by=id))

### End class declarations

# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()


# 

