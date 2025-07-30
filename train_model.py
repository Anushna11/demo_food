import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
client = MongoClient("mongodb://localhost:27017")
db = client["ml_app"]
collection = db["food_dataset"]

data = list(collection.find({}, {"_id": 0}))  
df = pd.DataFrame(data)

label_encoders = {}
encode_columns = ["mood", "time_of_day", "diet", "food_prediction"]

for col in encode_columns:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

if "food_prediction" in df.columns:
    X = df.drop(columns=["food_prediction"])
    y = df["food_prediction"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "food_model.pkl")
    joblib.dump(label_encoders, "label_encoders.pkl")

    accuracy = model.score(X_test, y_test)
    print(f"✅ Model trained successfully! Accuracy: {accuracy:.2f}")