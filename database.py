import pandas as pd
import json


class Dataset:
    def __init__(self):
        return self

    """
    It couldnt open normal file with read_json, so I have to read each line
    """
    def get_dataset_json(path):
        print("Getting json lines...")
        datasetJson = [json.loads(line) for line in open(path,'r')]
        return  datasetJson

    def get_data_len(datasetJson):
        return len(datasetJson)

    def get_unique_value(datasetJson, position):
        return datasetJson[position]

    def get_column_values(self, datasetJson):
        uniqueObj = self.get_unique_value(datasetJson, 0)
        return list(uniqueObj.keys())

    def construct_dataset(self, datasetJson):
        print("Constructing dataset...")
        dataLenght = self.get_data_len(datasetJson)
        colValues = self.get_column_values(self, datasetJson)
        emptyDataset = pd.DataFrame()

        i = 0
        for col in colValues:
            print(f"Making column {i}")
            values = []
            for position in range(dataLenght):
                uniqueObj = datasetJson[position]
                values.append(uniqueObj[col])

            emptyDataset[col] = values
            i += 1

        return emptyDataset
