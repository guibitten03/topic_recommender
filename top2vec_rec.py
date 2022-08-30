from top2vec_cpy import Top2Vec
import pandas as pd

class Top2vec_rec:
    def __init__(self) -> None:
        pass
    
    def fit(reviews_list, speed, workers) -> Top2Vec:
        model = Top2Vec(documents=reviews_list, 
                        speed=speed, 
                        workers=workers)
        
        return model
    
    def topics_to_pivot_matrix(model) -> pd.Dataframe:
        num_topics = model.get_num_topics()
        
        most
        