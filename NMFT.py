import pandas as pd
import numpy as np
import math
from mf import MF
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

class NMFT():
    def __init__(self, data, text_path, min_df, stop_words, nmf_components, random_state) -> None:
        self.data = data
        self.text_path = text_path
        self.min_df = min_df
        self.stop_words = stop_words
        self.nmf_components = nmf_components
        self.random_state = random_state
        
    
    def fit_transform(self):
        vect = TfidfVectorizer(min_df = self.min_df, stop_words=self.stop_words)

        variables = vect.fit_transform(self.data[self.text_path])
        
        model = NMF(n_components=self.nmf_components, random_state=self.random_state)

        model.fit(variables)
        features = model.transform(variables)
        self.features = features
        
    def user_similarity(u1, u2):
        u1Mean = u1.mean()
        u2Mean = u2.mean()
        
        numerator = 0
        denominator = 0
        for item in range(len(u1)):
            numerator += (u1[item] - u1Mean)*(u2[item] - u2Mean)
            
        for item in range(len(u1)):
            denominator += math.pow(u1[item] - u1Mean, 2) * math.pow(u2[item] - u2Mean, 2)
            
        denominator = math.sqrt(denominator)
        sim = numerator / denominator
        return sim
    
    def train(self):
        featuresDf = pd.DataFrame(self.features)
        featuresDf['user_id'] = self.data['user_id']
        featuresDf = featuresDf.groupby(by=['user_id']).sum().reset_index()
        
        userToRec = featuresDf.iloc[0, 1:]
        usersSim = []

        for user in range(1, featuresDf.shape[0]):
            userS = featuresDf.iloc[user, 1:]
            sim = self.user_similarity(userToRec, userS)
            usersSim.append(sim)
            
        
        similarsUsers = []

        for u in range(10):
            maximum = max(usersSim)
            maximum = usersSim.index(maximum)
            usersSim.pop(maximum)
            similarsUsers.append(maximum)
            print(maximum)
            
        for u in range(len(similarsUsers)):
            similarsUsers[u] = featuresDf.iloc[u, 0]


        mostSimilarDataset = self.data[['user_id', 'business_id', 'stars']]
        mostSimilarDataset = mostSimilarDataset.loc[mostSimilarDataset['user_id'].isin(similarsUsers)]
        mostSimilarDataset = pd.pivot_table(mostSimilarDataset, index='user_id', columns='business_id', values='stars')
        mostSimilarDataset.fillna(0)
        pivotMatrix = mostSimilarDataset.values
        pivotMatrix[np.isnan(pivotMatrix)] = 0
        
    
    def get_ratings():
        mfModel = MF(pivotMatrix, K = 10, alpha=0.1, beta=0.01, iterations=20)
        mfModel.train()