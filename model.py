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
    # ratings = relationship("Rating")

    # other_users = 

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


    def similarity_pairs(self, other_users, movie_id):
        similarity_pairs = []
        for u in other_users:
            pearson_coeff = self.similarity(u)
            for rating in u.ratings:
                if rating.movie_id == movie_id:
                    movie_rating = rating.rating
            if pearson_coeff > 0:        
                similarity_pairs.append((pearson_coeff, movie_rating))
        print "SIM PAIRS", similarity_pairs
        return similarity_pairs

    # def filter(movie_id):
    def make_prediction(self, movie_id):
        movie_ratings = session.query(Rating).filter_by(movie_id = movie_id).all()
        other_users = []
        # other_users = [other_users.append(rating.user) for rating in movie_ratings]
        for rating in movie_ratings:
            if rating.user_id != self.id:
                other_users.append(rating.user) 

    # def make_prediction(other_users)
        similarity_pairs = self.similarity_pairs(other_users, movie_id)
        coeff_sum = 0
        coeffs = 0
        for item in similarity_pairs:
            coeff_sum = coeff_sum + (item[0] * item[1])
            coeffs += item[0]
        weighted_mean = coeff_sum/coeffs
        return weighted_mean
        # return prediction

    # def similarity(self, other):
    #     u_ratings = {}
    #     paired_ratings = []
    #     for r in self.ratings:
    #         u_ratings[r.movie_id] = r

    #     for r in other.ratings:
    #         u_r = u_ratings.get(r.movie_id)
    #         if u_r:
    #             paired_ratings.append( (u_r.rating, r.rating) )

    #     if paired_ratings:
    #         return correlation.pearson(paired_ratings)
    #     else:
    #         return 0.0

    # def predict_rating(self, movie):
    #     ratings = self.ratings
    #     other_ratings = movie.ratings
    #     similarities = [ (self.similarity(r.user), r) \
    #         for r in other_ratings ]
    #     similarities.sort(reverse = True)
    #     similarities = [ sim for sim in similarities if sim[0] > 0 ]
    #     if not similarities:
    #         return None
    #     numerator = sum([ r.rating * similarity for similarity, r in similarities ])
    #     denominator = sum([ similarity[0] for similarity in similarities ])
    #     return numerator/denominator



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
    user = relationship("User",
        backref=backref("ratings", order_by=id))

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

