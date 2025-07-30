import pymongo
import pandas as pd
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["ml_app"]
collection=db["food_dataset"]
df=pd.read_csv("food_dataset.csv")
rec=df.to_dict(orient="records")
collection.insert_many(rec)
