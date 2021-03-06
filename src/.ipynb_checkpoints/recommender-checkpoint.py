import logging
import numpy as np
import pandas as pd

# Spark imports
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from ast import literal_eval


class MovieRecommender():
    """Template class for a Movie Recommender system."""

    def __init__(self):
        """Constructs a MovieRecommender"""
        self.logger = logging.getLogger('reco-cs')
        self.model = ALS(userCol='user',
                itemCol='movie',
                ratingCol='rating',
                nonnegative=True,
                regParam=0.1,
                rank=10)
        
        self.user_factors_df = pd.read_csv('data/user_factors.csv', index_col='id')
        self.movie_factors_df = pd.read_csv('data/movie_factors.csv', index_col='id')
        

    def fit(self, ratings):
        """
        Trains the recommender on a given set of ratings.

        Parameters
        ----------
        ratings : pandas dataframe, shape = (n_ratings, 4)
                  with columns 'user', 'movie', 'rating', 'timestamp'

        Returns
        -------
        self : object
            Returns self.
        """
        self.logger.debug("starting fit")

        spark = SparkSession.builder.getOrCreate()
        spark_df = spark.createDataFrame(ratings)
        spark_df = spark_df.drop('timestamp')
        
#         # train/validation split
#         train, validation = spark_df.randomSplit([0.8, 0.2])
        self.recommender = self.model.fit(spark_df)

        self.logger.debug("finishing fit")
        return(self)
    
    
    def predicted_rating(user_id, movie_id):
        """
        Gets the user and movie features from the save csv files. 
        If user and/or movie not found, estimate latent features based on neighbors
        
        Inputs:
        user_id: int
        movie_id: int
        
        Returns:
        predicted rating: float        
        """
        
        try:
            # Get features from df and turn from string into list
            u_features = literal_eval(self.user_factors_df.loc[user_id, 'features'])
            user = np.array(u_features)
        except:
            user = find_similar_users(user_id)

        try:
            i_features = literal_eval(self.movie_factors_df.loc[movie_id, 'features'])
            item = np.array(i_features)
        except:
            item = find_similar_items(movie_id)

        # Check if they are same shape
        if user.shape == item.shape:
            return np.dot(np.array(user), np.array(item))
        else:
            return -1


    def find_similar_users(user_id):
        """
        Finds similar users and returns best guess for cosine similarity matrix
    
        Inputs:
        user_id: int
            
        """
        if len(self.user_factors_df.colums) == 2:
            self.user_factors_df.drop('Unnamed: 0', axis=1)
    
        similar_user_ids = self.users_sim_mat.loc[round(self.users_sim_mat[user_id].sort_values(ascending=False), 5) >= 1][1:].index.values
    
        users = []
    
        for i in similar_user_ids:
            try:
                u_features = literal_eval(self.user_factors_df.loc[i, 'features'])
                user = np.array(u_features)
                users.append(user)
            except:
                continue

        return np.mean(users, axis=0)


    def find_similar_items(movie_id):
        """
        Find similar movies and returns best guess for cosine similarity matrix
    
        Inputs:
        movie_id: int
    
        """
        similar_movie_ids = self.movies_sim_mat.loc[round(self.movies_sim_mat[movie_id].sort_values(ascending=False), 5) >= 1][1:].index.values
    
        items = []

        for i in similar_movie_ids:
            i_features = literal_eval(movie_factors_df.loc[i, 'features'])
            item = np.array(i_features)
            items.append(item)

        return np.mean(items, axis=0)

    
    def out_of_bounds(df):
        """Fixes predicted ratings that are > 5 or < 1
        """
        df.loc[df['rating']<1, 'rating'] = 1
        df.loc[df['rating']>5, 'rating'] = 5
        
        # Sort values and replace rating with title
        df = df.sort_values(by=['user', 'rating'], ascending=[True, False])
                       
        return df
    

            
    def transform(self, requests):
        """
        Predicts the ratings for a given set of requests.

        Parameters
        ----------
        requests : pandas dataframe, shape = (n_ratings, 2)
                  with columns 'user', 'movie'

        Returns
        -------
        dataframe : a pandas dataframe with columns 'user', 'movie', 'rating'
                    column 'rating' containing the predicted rating
        """
        self.logger.debug("starting predict")
        self.logger.debug("request count: {}".format(requests.shape[0]))

        requests['rating'] = np.random.choice(range(1, 5), requests.shape[0])

        # Get predicted ratings
#        requests['rating'] = requests.apply(lambda x: predicted_rating(x['user'], 
#                                                                       x['movie']), axis=1)

        # Fix out of bounds ratings, create movie ranking
#        requests = out_of_bounds(requests)



        self.logger.debug("finishing predict")
        return(requests)
        


if __name__ == "__main__":
    logger = logging.getLogger('reco-cs')
    logger.critical('you should use run.py instead')
