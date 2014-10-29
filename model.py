from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation

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

    def similarity(self, user2):
        user_ratings = {}
        rating_pairs = []
        for r in self.ratings:
            user_ratings[r.movie_id] = r.rating

        for r in user2.ratings:
            if r.movie_id in user_ratings:
                rating_pairs.append((r.rating, user_ratings[r.movie_id]))

        if rating_pairs:
            return correlation.pearson(rating_pairs)
        else:
            return 0.0

    def ranked_users(self, other_users):
        rankings = []
        for u in other_users:
            pearson_coeff = self.similarity(u)
            rankings.append((pearson_coeff, u.id))
        return sorted(rankings[0])

    def make_prediction(self, other_users, movie):
        top_user = ranked_users(other_users)
        for rating in top_user.ratings:




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
u = session.query(User).get(1)
u2 = session.query(User).get(2)
u3 = session.query(User).get(3)
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

