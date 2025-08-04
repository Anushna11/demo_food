import streamlit as st
import pymongo
import requests
 
client = pymongo.MongoClient("mongodb+srv://anushna:Qu6pY3fU2I7hsCS3@cluster1.sjmrtri.mongodb.net/")
db = client["Food_prediction"]
collection = db["users"]
prediction_collection = db["predictions"]   
 
ADMIN_USERNAME = "anu"
ADMIN_PASSWORD = "anu"

st.title("🍽️ Food Predictor 😋")
select = st.sidebar.selectbox("Page Navigator", ["Registration Page", "Prediction Page", "Admin Page"])
if select == "Registration Page":
    st.header("📝 Registration Page")
    un = st.text_input("Choose a Username")
    pw = st.text_input("Choose a Password", type="password")
    bn = st.button("Register")
    if bn:
        if un != "" and pw != "":
            e_user = collection.find_one({"username": un, "password": pw})
            if e_user:
                st.error("❌ Username and password already exist")
            else:
                collection.insert_one({
                    "username": un,
                    "password": pw,
                    "Predicted_food": None
                })
                st.success("✅ Registration successful!")
        else:
            st.error("⚠️ Enter a proper username and password")
 
elif select == "Prediction Page":
    st.header("🔐 Login to Predict Your Food")

    un = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if un != "" and pw != "":
        user = collection.find_one({"username": un, "password": pw})

        if user:
            st.markdown("---")
            st.header(f"👋 Hi {un}, predict your food preference")
            mood = st.selectbox("Mood", ["happy", "tired", "sad", "energetic", "bored", "angry", "neutral", "excited", "stressed"])
            time_of_day = st.selectbox("Time of Day", ["breakfast", "lunch", "evening", "dinner"])
            diet = st.selectbox("Choose your diet", ["veg", "non-veg", "vegan"])
            is_hungry = st.checkbox("Are you hungry?")
            prefers_spicy = st.checkbox("Prefer spicy?")

            if st.button("🍲 Predict the Food"):
                data = {
                    "mood": mood,
                    "time_of_day": time_of_day,
                    "is_hungry": is_hungry,
                    "prefers_spicy": prefers_spicy,
                    "diet": diet
                }

                try:
                    res = requests.post("https://demo-food-3.onrender.com/predict", json=data)
                    result = res.json()
                    predicted_food = result.get("Predicted_food", "None")
                    st.success(f"🍛 Predicted Food: {predicted_food}")
                    collection.update_one(
                        {"username": un},
                        {"$set": {"Predicted_food": predicted_food}}
                    )
                    prediction_collection.insert_one({
                        "username": un,
                        "prediction": predicted_food,
                        "details": data
                    })

                except Exception as e:
                    st.error(f"Prediction failed: {e}")
        else:
            st.error("❌ Invalid username or password")
elif select == "Admin Page":
    st.header("👨‍💼 Admin Login")

    un = st.text_input("Admin Username")
    pw = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if un == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
            st.success("✅ Admin Login Successful")
            st.subheader("📋 Registered Users & Prediction Data")

            data = collection.find()
            for record in data:
                st.write(f"👤 Username: {record.get('username')}")
                st.write(f"🔒 Password: {record.get('password')}")
                st.write(f"🍽️ Predicted Food: {record.get('Predicted_food')}")
                st.markdown("---")
        else:
            st.error("❌ Invalid Admin Credentials")

