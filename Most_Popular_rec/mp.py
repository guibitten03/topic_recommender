import pandas as pd
from database import Dataset

class MP():
    
    def __init__(self, data:pd.DataFrame, user:str, model:str, nbRecommendations:int):
        self.data = data
        self.user = user
        self.model = model.lower()
        self.nb = nbRecommendations
        
        
    def __get_recommender(self) -> list:
        userVisited = self.data.loc[self.data['user_id'] == self.user]
        visitedBusUser = list(userVisited['business_id'])
        
        busToRec = []
        for item in range(self.nb):
            if not (self.filtedData[item] in visitedBusUser):
                busToRec.append(self.populars[item])
            else:
                item -= 1
                
        return busToRec
    
    
    def recommender(self) -> list:

        mpDataset = self.data[['business_id', 'stars']].copy()
        
        if self.model == 'popular':
            self.filtedData = mpDataset.groupby(by=['business_id']).size().sort_values(ascending=False).index
            busToRec = self.__get_recommender(self)
            return busToRec
        
        if self.model == 'rated':
            mostRatedBusiness = mpDataset.groupby(by=['business_id']).sum().sort_values(by=['stars'], ascending=False).reset_index()
            self.filtedData = mostRatedBusiness['business_id'].values
            busToRec = self.__get_recommender(self)
            return busToRec