import logging
import numpy as np
import pandas as pd

from ast import literal_eval



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
        u_features = literal_eval(user_factors_df.loc[user_id, 'features'])
        user = np.array(u_features)
    except:
        user = find_similar_users(user_id)
            
    try:
        i_features = literal_eval(movie_factors_df.loc[movie_id, 'features'])
        item = np.array(i_features)
    except:
        item = find_similar_items(movie_id)
        
    if user.shape == item.shape:
        return np.dot(np.array(user), np.array(item))
    else:
        return -1    
    
def find_similar_users(user_id):
    return np.array(-1)
    
def find_similar_items(movie_id):
    return np.array(1)


def out_of_bounds(df):
    """Fixes predicted ratings that are > 5 or < 1
    """
    df.loc[df['rating']<1, 'rating'] = 1
    df.loc[df['rating']>5, 'rating'] = 5
        
    # Sort values and replace rating with title
    df = df.sort_values(by=['user', 'rating'], ascending=[True, False])
    df['movie'] = df.apply(lambda x: find_movie(x['movie']), axis=1)
                
    return df    
    
    
def find_movie(movie_id):
    return 'movie' 


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

    requests['rating'] = np.random.choice(range(1, 5), requests.shape[0])

        # Get predicted ratings
#        requests['rating'] = requests.apply(lambda x: predicted_rating(x['user'], 
#                                                                       x['movie']), axis=1)

        # Fix out of bounds ratings, create movie ranking
#        requests = out_of_bounds(requests)

    return requests